#===============================================================================
# Copyright (C) 2014 Ryan Holmes
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import re
import os
import xml.dom

from eos.types import State, Slot, Module, Cargo, Fit, Ship, Drone, Implant, Booster
import service
import wx
import logging
import config
import collections
import json

logger = logging.getLogger("pyfa.service.port")

try:
    from collections import OrderedDict
except ImportError:
    from utils.compat import OrderedDict

EFT_SLOT_ORDER = [Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM]
INV_FLAGS = {
            Slot.LOW: 11,
            Slot.MED: 19,
            Slot.HIGH: 27,
            Slot.RIG: 92,
            Slot.SUBSYSTEM: 125}

INV_FLAG_CARGOBAY = 5
INV_FLAG_DRONEBAY = 87

class Port(object):
    """Service which houses all import/export format functions"""
    @classmethod
    def exportCrest(cls, ofit, callback=None):
        # A few notes:
        # max fit name length is 50 characters
        # Most keys are created simply because they are required, but bogus data is okay

        nested_dict = lambda: collections.defaultdict(nested_dict)
        fit = nested_dict()
        sCrest = service.Crest.getInstance()
        sFit = service.Fit.getInstance()

        eve = sCrest.eve

        # max length is 50 characters
        name = ofit.name[:47] + '...' if len(ofit.name) > 50 else ofit.name
        fit['name'] = name
        fit['ship']['href'] = "%sinventory/types/%d/"%(eve._authed_endpoint, ofit.ship.item.ID)
        fit['ship']['id'] = ofit.ship.item.ID
        fit['ship']['name'] = ''

        fit['description'] = "<pyfa:%d />"%ofit.ID
        fit['items'] = []

        slotNum = {}
        charges = {}
        for module in ofit.modules:
            if module.isEmpty:
                continue

            item = nested_dict()
            slot = module.slot

            if slot == Slot.SUBSYSTEM:
                # Order of subsystem matters based on this attr. See GH issue #130
                slot = int(module.getModifiedItemAttr("subSystemSlot"))
                item['flag'] = slot
            else:
                if not slot in slotNum:
                    slotNum[slot] = INV_FLAGS[slot]

                item['flag'] = slotNum[slot]
                slotNum[slot] += 1

            item['quantity'] = 1
            item['type']['href'] = "%sinventory/types/%d/"%(eve._authed_endpoint, module.item.ID)
            item['type']['id'] = module.item.ID
            item['type']['name'] = ''
            fit['items'].append(item)

            if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                if not module.chargeID in charges:
                    charges[module.chargeID] = 0
                # `or 1` because some charges (ie scripts) are without qty
                charges[module.chargeID] += module.numCharges or 1

        for cargo in ofit.cargo:
            item = nested_dict()
            item['flag'] = INV_FLAG_CARGOBAY
            item['quantity'] = cargo.amount
            item['type']['href'] = "%sinventory/types/%d/"%(eve._authed_endpoint, cargo.item.ID)
            item['type']['id'] = cargo.item.ID
            item['type']['name'] = ''
            fit['items'].append(item)

        for chargeID, amount in charges.items():
            item = nested_dict()
            item['flag'] = INV_FLAG_CARGOBAY
            item['quantity'] = amount
            item['type']['href'] = "%sinventory/types/%d/"%(eve._authed_endpoint, chargeID)
            item['type']['id'] = chargeID
            item['type']['name'] = ''
            fit['items'].append(item)

        for drone in ofit.drones:
            item = nested_dict()
            item['flag'] = INV_FLAG_DRONEBAY
            item['quantity'] = drone.amount
            item['type']['href'] = "%sinventory/types/%d/"%(eve._authed_endpoint, drone.item.ID)
            item['type']['id'] = drone.item.ID
            item['type']['name'] = ''
            fit['items'].append(item)

        return json.dumps(fit)

    @classmethod
    def importAuto(cls, string, path=None, activeFit=None, callback=None, encoding=None):
        # Get first line and strip space symbols of it to avoid possible detection errors
        firstLine = re.split("[\n\r]+", string.strip(), maxsplit=1)[0]
        firstLine = firstLine.strip()

        # If XML-style start of tag encountered, detect as XML
        if re.match("<", firstLine):
            if encoding:
                return "XML", cls.importXml(string, callback, encoding)
            else:
                return "XML", cls.importXml(string, callback)

        # If JSON-style start, parse as CREST/JSON
        if firstLine[0] == '{':
            return "JSON", (cls.importCrest(string),)

        # If we've got source file name which is used to describe ship name
        # and first line contains something like [setup name], detect as eft config file
        if re.match("\[.*\]", firstLine) and path is not None:
            filename = os.path.split(path)[1]
            shipName = filename.rsplit('.')[0]
            return "EFT Config", cls.importEftCfg(shipName, string, callback)

        # If no file is specified and there's comma between brackets,
        # consider that we have [ship, setup name] and detect like eft export format
        if re.match("\[.*,.*\]", firstLine):
            return "EFT", (cls.importEft(string),)

        # Use DNA format for all other cases
        return "DNA", (cls.importDna(string),)

    @staticmethod
    def importCrest(str):
        fit = json.loads(str)
        sMkt = service.Market.getInstance()

        f = Fit()
        f.name = fit['name']

        try:
            f.ship = Ship(sMkt.getItem(fit['ship']['id']))
        except:
            return None

        items = fit['items']
        items.sort(key=lambda k: k['flag'])

        moduleList = []
        for module in items:
            try:
                item = sMkt.getItem(module['type']['id'], eager="group.category")
                if module['flag'] == INV_FLAG_DRONEBAY:
                    d = Drone(item)
                    d.amount = module['quantity']
                    f.drones.append(d)
                elif module['flag'] == INV_FLAG_CARGOBAY:
                    c = Cargo(item)
                    c.amount = module['quantity']
                    f.cargo.append(c)
                else:
                    try:
                        m = Module(item)
                    # When item can't be added to any slot (unknown item or just charge), ignore it
                    except ValueError:
                        continue
                    # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                    if item.category.name == "Subsystem":
                        if m.fits(f):
                            f.modules.append(m)
                    else:
                        if m.isValidState(State.ACTIVE):
                            m.state = State.ACTIVE

                        moduleList.append(m)

            except:
                continue

        # Recalc to get slot numbers correct for T3 cruisers
        service.Fit.getInstance().recalc(f)

        for module in moduleList:
            if module.fits(f):
                f.modules.append(module)

        return f

    @staticmethod
    def importDna(string):
        sMkt = service.Market.getInstance()

        ids = map(int, re.findall(r'\d+', string))
        for id in ids:
            try:
                Ship(sMkt.getItem(id))
                string = string[string.index(str(id)):]
                break
            except:
                pass
        string = string[:string.index("::") + 2]
        info = string.split(":")

        f = Fit()
        try:
            f.ship = Ship(sMkt.getItem(int(info[0])))
            f.name = "{0} - DNA Imported".format(f.ship.item.name)
        except UnicodeEncodeError as e:
            def logtransform(s):
                if len(s) > 10:
                    return s[:10] + "..."
                return s
            logger.exception("Couldn't import ship data %r", [ logtransform(s) for s in info ])
            return None

        moduleList = []
        for itemInfo in info[1:]:
            if itemInfo:
                itemID, amount = itemInfo.split(";")
                item = sMkt.getItem(int(itemID), eager="group.category")

                if item.category.name == "Drone":
                    d = Drone(item)
                    d.amount = int(amount)
                    f.drones.append(d)
                elif item.category.name == "Charge":
                    c = Cargo(item)
                    c.amount = int(amount)
                    f.cargo.append(c)
                else:
                    for i in xrange(int(amount)):
                        try:
                            m = Module(item)
                        except:
                            continue
                        # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                        if item.category.name == "Subsystem":
                            if m.fits(f):
                                f.modules.append(m)
                        else:
                            m.owner = f
                            if m.isValidState(State.ACTIVE):
                                m.state = State.ACTIVE
                            moduleList.append(m)

        # Recalc to get slot numbers correct for T3 cruisers
        service.Fit.getInstance().recalc(f)

        for module in moduleList:
            if module.fits(f):
                module.owner = f
                if module.isValidState(State.ACTIVE):
                    module.state = State.ACTIVE
                f.modules.append(module)

        return f

    @staticmethod
    def importEft(eftString):
        sMkt = service.Market.getInstance()
        offineSuffix = " /OFFLINE"

        fit = Fit()
        eftString = eftString.strip()
        lines = re.split('[\n\r]+', eftString)
        info = lines[0][1:-1].split(",", 1)

        if len(info) == 2:
            shipType = info[0].strip()
            fitName = info[1].strip()
        else:
            shipType = info[0].strip()
            fitName = "Imported %s" % shipType

        try:
            ship = sMkt.getItem(shipType)
            fit.ship = Ship(ship)
            fit.name = fitName
        except:
            return

        # maintain map of drones and their quantities
        droneMap = {}
        cargoMap = {}
        moduleList = []
        for i in range(1, len(lines)):
            ammoName = None
            extraAmount = None

            line = lines[i].strip()
            if not line:
                continue

            setOffline = line.endswith(offineSuffix)
            if setOffline is True:
                # remove offline suffix from line
                line = line[:len(line) - len(offineSuffix)]

            modAmmo = line.split(",")
            # matches drone and cargo with x{qty}
            modExtra = modAmmo[0].split(" x")

            if len(modAmmo) == 2:
                # line with a module and ammo
                ammoName = modAmmo[1].strip()
                modName = modAmmo[0].strip()
            elif len(modExtra) == 2:
                # line with drone/cargo and qty
                extraAmount = modExtra[1].strip()
                modName = modExtra[0].strip()
            else:
                # line with just module
                modName = modExtra[0].strip()

            try:
                # get item information. If we are on a Drone/Cargo line, throw out cargo
                item = sMkt.getItem(modName, eager="group.category")
            except:
                # if no data can be found (old names)
                continue

            if item.category.name == "Drone":
                extraAmount = int(extraAmount) if extraAmount is not None else 1
                if not modName in droneMap:
                    droneMap[modName] = 0
                droneMap[modName] += extraAmount
            if len(modExtra) == 2 and item.category.name != "Drone":
                extraAmount = int(extraAmount) if extraAmount is not None else 1
                if not modName in cargoMap:
                    cargoMap[modName] = 0
                cargoMap[modName] += extraAmount
            elif item.category.name == "Implant":
                fit.implants.append(Implant(item))
            # elif item.category.name == "Subsystem":
            #     try:
            #         subsystem = Module(item)
            #     except ValueError:
            #         continue
            #
            #     if subsystem.fits(fit):
            #         fit.modules.append(subsystem)
            else:
                try:
                    m = Module(item)
                except ValueError:
                    continue
                # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                if item.category.name == "Subsystem":
                    if m.fits(fit):
                        fit.modules.append(m)
                else:
                    if ammoName:
                        try:
                            ammo = sMkt.getItem(ammoName)
                            if m.isValidCharge(ammo) and m.charge is None:
                                m.charge = ammo
                        except:
                            pass

                    if setOffline is True and m.isValidState(State.OFFLINE):
                        m.state = State.OFFLINE
                    elif m.isValidState(State.ACTIVE):
                        m.state = State.ACTIVE

                    moduleList.append(m)

        # Recalc to get slot numbers correct for T3 cruisers
        service.Fit.getInstance().recalc(fit)

        for m in moduleList:
            if m.fits(fit):
                m.owner = fit
                if not m.isValidState(m.state):
                    print "Error: Module", m, "cannot have state", m.state

                fit.modules.append(m)

        for droneName in droneMap:
            d = Drone(sMkt.getItem(droneName))
            d.amount = droneMap[droneName]
            fit.drones.append(d)

        for cargoName in cargoMap:
            c = Cargo(sMkt.getItem(cargoName))
            c.amount = cargoMap[cargoName]
            fit.cargo.append(c)

        return fit

    @staticmethod
    def importEftCfg(shipname, contents, callback=None):
        """Handle import from EFT config store file"""

        # Check if we have such ship in database, bail if we don't
        sMkt = service.Market.getInstance()
        try:
            sMkt.getItem(shipname)
        except:
            return []  # empty list is expected

        # If client didn't take care of encoding file contents into Unicode,
        # do it using fallback encoding ourselves
        if isinstance(contents, str):
            contents = unicode(contents, "cp1252")

        fits = []  # List for fits
        fitIndices = []  # List for starting line numbers for each fit
        lines = re.split('[\n\r]+', contents)  # Separate string into lines

        for line in lines:
            # Detect fit header
            if line[:1] == "[" and line[-1:] == "]":
                # Line index where current fit starts
                startPos = lines.index(line)
                fitIndices.append(startPos)

        for i, startPos in enumerate(fitIndices):
            # End position is last file line if we're trying to get it for last fit,
            # or start position of next fit minus 1
            endPos = len(lines) if i == len(fitIndices) - 1 else fitIndices[i + 1]

            # Finally, get lines for current fitting
            fitLines = lines[startPos:endPos]

            try:
                # Create fit object
                f = Fit()
                # Strip square brackets and pull out a fit name
                f.name = fitLines[0][1:-1]
                # Assign ship to fitting
                f.ship = Ship(sMkt.getItem(shipname))

                moduleList = []
                for x in range(1, len(fitLines)):
                    line = fitLines[x]
                    if not line:
                        continue

                    # Parse line into some data we will need
                    misc = re.match("(Drones|Implant|Booster)_(Active|Inactive)=(.+)", line)
                    cargo = re.match("Cargohold=(.+)", line)

                    if misc:
                        entityType = misc.group(1)
                        entityState = misc.group(2)
                        entityData = misc.group(3)
                        if entityType == "Drones":
                            droneData = re.match("(.+),([0-9]+)", entityData)
                            # Get drone name and attempt to detect drone number
                            droneName = droneData.group(1) if droneData else entityData
                            droneAmount = int(droneData.group(2)) if droneData else 1
                            # Bail if we can't get item or it's not from drone category
                            try:
                                droneItem = sMkt.getItem(droneName, eager="group.category")
                            except:
                                continue
                            if droneItem.category.name != "Drone":
                                continue
                            # Add drone to the fitting
                            d = Drone(droneItem)
                            d.amount = droneAmount
                            if entityState == "Active":
                                d.amountActive = droneAmount
                            elif entityState == "Inactive":
                                d.amountActive = 0
                            f.drones.append(d)
                        elif entityType == "Implant":
                            # Bail if we can't get item or it's not from implant category
                            try:
                                implantItem = sMkt.getItem(entityData, eager="group.category")
                            except:
                                continue
                            if implantItem.category.name != "Implant":
                                continue
                            # Add implant to the fitting
                            imp = Implant(implantItem)
                            if entityState == "Active":
                                imp.active = True
                            elif entityState == "Inactive":
                                imp.active = False
                            f.implants.append(imp)
                        elif entityType == "Booster":
                            # Bail if we can't get item or it's not from implant category
                            try:
                                boosterItem = sMkt.getItem(entityData, eager="group.category")
                            except:
                                continue
                            # All boosters have implant category
                            if boosterItem.category.name != "Implant":
                                continue
                            # Add booster to the fitting
                            b = Booster(boosterItem)
                            if entityState == "Active":
                                b.active = True
                            elif entityState == "Inactive":
                                b.active = False
                            f.boosters.append(b)
                    # If we don't have any prefixes, then it's a module
                    elif cargo:
                        cargoData = re.match("(.+),([0-9]+)", cargo.group(1))
                        cargoName = cargoData.group(1) if cargoData else cargo.group(1)
                        cargoAmount = int(cargoData.group(2)) if cargoData else 1
                        # Bail if we can't get item
                        try:
                            item = sMkt.getItem(cargoName)
                        except:
                            continue
                        # Add Cargo to the fitting
                        c = Cargo(item)
                        c.amount = cargoAmount
                        f.cargo.append(c)
                    else:
                        withCharge = re.match("(.+),(.+)", line)
                        modName = withCharge.group(1) if withCharge else line
                        chargeName = withCharge.group(2) if withCharge else None
                        # If we can't get module item, skip it
                        try:
                            modItem = sMkt.getItem(modName)
                        except:
                            continue

                        # Create module
                        m = Module(modItem)

                        # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                        if modItem.category.name == "Subsystem":
                            if m.fits(f):
                                f.modules.append(m)
                        else:
                            m.owner = f
                            # Activate mod if it is activable
                            if m.isValidState(State.ACTIVE):
                                m.state = State.ACTIVE
                            # Add charge to mod if applicable, on any errors just don't add anything
                            if chargeName:
                                try:
                                    chargeItem = sMkt.getItem(chargeName, eager="group.category")
                                    if chargeItem.category.name == "Charge":
                                        m.charge = chargeItem
                                except:
                                    pass
                            # Append module to fit
                            moduleList.append(m)

                # Recalc to get slot numbers correct for T3 cruisers
                service.Fit.getInstance().recalc(f)

                for module in moduleList:
                    if module.fits(f):
                        f.modules.append(module)

                # Append fit to list of fits
                fits.append(f)

                if callback:
                    wx.CallAfter(callback, None)
            # Skip fit silently if we get an exception
            except Exception:
                pass

        return fits

    @staticmethod
    def importXml(text, callback=None, encoding="utf-8"):
        sMkt = service.Market.getInstance()

        doc = xml.dom.minidom.parseString(text.encode(encoding))
        fittings = doc.getElementsByTagName("fittings").item(0)
        fittings = fittings.getElementsByTagName("fitting")
        fits = []

        for i, fitting in enumerate(fittings):
            f = Fit()
            f.name = fitting.getAttribute("name")
            # <localized hint="Maelstrom">Maelstrom</localized>
            shipType = fitting.getElementsByTagName("shipType").item(0).getAttribute("value")
            try:
                f.ship = Ship(sMkt.getItem(shipType))
            except:
                continue
            hardwares = fitting.getElementsByTagName("hardware")
            moduleList = []
            for hardware in hardwares:
                try:
                    moduleName = hardware.getAttribute("type")
                    try:
                        item = sMkt.getItem(moduleName, eager="group.category")
                    except:
                        continue
                    if item:
                        if item.category.name == "Drone":
                            d = Drone(item)
                            d.amount = int(hardware.getAttribute("qty"))
                            f.drones.append(d)
                        elif hardware.getAttribute("slot").lower() == "cargo":
                            # although the eve client only support charges in cargo, third-party programs
                            # may support items or "refits" in cargo. Support these by blindly adding all
                            # cargo, not just charges
                            c = Cargo(item)
                            c.amount = int(hardware.getAttribute("qty"))
                            f.cargo.append(c)
                        else:
                            try:
                                m = Module(item)
                            # When item can't be added to any slot (unknown item or just charge), ignore it
                            except ValueError:
                                continue
                            # Add subsystems before modules to make sure T3 cruisers have subsystems installed
                            if item.category.name == "Subsystem":
                                if m.fits(f):
                                    m.owner = f
                                    f.modules.append(m)
                            else:
                                if m.isValidState(State.ACTIVE):
                                    m.state = State.ACTIVE

                                moduleList.append(m)

                except KeyboardInterrupt:
                    continue

            # Recalc to get slot numbers correct for T3 cruisers
            service.Fit.getInstance().recalc(f)

            for module in moduleList:
                if module.fits(f):
                    module.owner = f
                    f.modules.append(module)

            fits.append(f)
            if callback:
                wx.CallAfter(callback, None)

        return fits

    @staticmethod
    def _exportEftBase(fit):
        offineSuffix = " /OFFLINE"
        export = "[%s, %s]\n" % (fit.ship.item.name, fit.name)
        stuff = {}
        sFit = service.Fit.getInstance()
        for module in fit.modules:
            slot = module.slot
            if not slot in stuff:
                stuff[slot] = []
            curr = module.item.name if module.item else ("[Empty %s slot]" % Slot.getName(slot).capitalize() if slot is not None else "")
            if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                curr += ", %s" % module.charge.name
            if module.state == State.OFFLINE:
                curr += offineSuffix
            curr += "\n"
            stuff[slot].append(curr)

        for slotType in EFT_SLOT_ORDER:
            data = stuff.get(slotType)
            if data is not None:
                export += "\n"
                for curr in data:
                    export += curr

        if len(fit.drones) > 0:
            export += "\n\n"
            for drone in fit.drones:
                export += "%s x%s\n" % (drone.item.name, drone.amount)

        if len(fit.fighters) > 0:
            export += "\n\n"
            for fighter in fit.fighters:
                export += "%s x%s\n" % (fighter.item.name, fighter.amountActive)

        if export[-1] == "\n":
            export = export[:-1]

        return export

    @classmethod
    def exportEft(cls, fit):
        export = cls._exportEftBase(fit)

        if len(fit.cargo) > 0:
            export += "\n\n\n"
            for cargo in fit.cargo:
                export += "%s x%s\n" % (cargo.item.name, cargo.amount)
        if export[-1] == "\n":
            export = export[:-1]

        return export

    @classmethod
    def exportEftImps(cls, fit):
        export = cls._exportEftBase(fit)

        if len(fit.implants) > 0:
            export += "\n\n\n"
            for implant in fit.implants:
                export += "%s\n" % implant.item.name
        if export[-1] == "\n":
            export = export[:-1]

        if len(fit.cargo) > 0:
            export += "\n\n\n"
            for cargo in fit.cargo:
                export += "%s x%s\n" % (cargo.item.name, cargo.amount)
        if export[-1] == "\n":
            export = export[:-1]

        return export

    @staticmethod
    def exportDna(fit):
        dna = str(fit.shipID)
        subsystems = []  # EVE cares which order you put these in
        mods = OrderedDict()
        charges = OrderedDict()
        for mod in fit.modules:
            if not mod.isEmpty:
                if mod.slot == Slot.SUBSYSTEM:
                    subsystems.append(mod)
                    continue
                if not mod.itemID in mods:
                    mods[mod.itemID] = 0
                mods[mod.itemID] += 1

                if mod.charge:
                    if not mod.chargeID in charges:
                        charges[mod.chargeID] = 0
                    # `or 1` because some charges (ie scripts) are without qty
                    charges[mod.chargeID] += mod.numCharges or 1

        for subsystem in sorted(subsystems, key=lambda mod: mod.getModifiedItemAttr("subSystemSlot")):
            dna += ":{0};1".format(subsystem.itemID)

        for mod in mods:
            dna += ":{0};{1}".format(mod, mods[mod])

        for drone in fit.drones:
            dna += ":{0};{1}".format(drone.itemID, drone.amount)

        for cargo in fit.cargo:
            # DNA format is a simple/dumb format. As CCP uses the slot information of the item itself
            # without designating slots in the DNA standard, we need to make sure we only include
            # charges in the DNA export. If modules were included, the EVE Client will interpret these
            # as being "Fitted" to whatever slot they are for, and it causes an corruption error in the
            # client when trying to save the fit
            if cargo.item.category.name == "Charge":
                if not cargo.item.ID in charges:
                    charges[cargo.item.ID] = 0
                charges[cargo.item.ID] += cargo.amount

        for charge in charges:
            dna += ":{0};{1}".format(charge, charges[charge])

        return dna + "::"

    @classmethod
    def exportXml(cls, callback=None, *fits):
        doc = xml.dom.minidom.Document()
        fittings = doc.createElement("fittings")
        doc.appendChild(fittings)
        sFit = service.Fit.getInstance()

        for i, fit in enumerate(fits):
            try:
                fitting = doc.createElement("fitting")
                fitting.setAttribute("name", fit.name)
                fittings.appendChild(fitting)
                description = doc.createElement("description")
                description.setAttribute("value", "")
                fitting.appendChild(description)
                shipType = doc.createElement("shipType")
                shipType.setAttribute("value", fit.ship.item.name)
                fitting.appendChild(shipType)

                charges = {}
                slotNum = {}
                for module in fit.modules:
                    if module.isEmpty:
                        continue

                    slot = module.slot

                    if slot == Slot.SUBSYSTEM:
                        # Order of subsystem matters based on this attr. See GH issue #130
                        slotId = module.getModifiedItemAttr("subSystemSlot") - 125
                    else:
                        if not slot in slotNum:
                            slotNum[slot] = 0

                        slotId = slotNum[slot]
                        slotNum[slot] += 1

                    hardware = doc.createElement("hardware")
                    hardware.setAttribute("type", module.item.name)
                    slotName = Slot.getName(slot).lower()
                    slotName = slotName if slotName != "high" else "hi"
                    hardware.setAttribute("slot", "%s slot %d" % (slotName, slotId))
                    fitting.appendChild(hardware)

                    if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                        if not module.charge.name in charges:
                            charges[module.charge.name] = 0
                        # `or 1` because some charges (ie scripts) are without qty
                        charges[module.charge.name] += module.numCharges or 1

                for drone in fit.drones:
                    hardware = doc.createElement("hardware")
                    hardware.setAttribute("qty", "%d" % drone.amount)
                    hardware.setAttribute("slot", "drone bay")
                    hardware.setAttribute("type", drone.item.name)
                    fitting.appendChild(hardware)

                for cargo in fit.cargo:
                    if not cargo.item.name in charges:
                        charges[cargo.item.name] = 0
                    charges[cargo.item.name] += cargo.amount

                for name, qty in charges.items():
                    hardware = doc.createElement("hardware")
                    hardware.setAttribute("qty", "%d" % qty)
                    hardware.setAttribute("slot", "cargo")
                    hardware.setAttribute("type", name)
                    fitting.appendChild(hardware)
            except:
                print "Failed on fitID: %d"%fit.ID
                continue
            finally:
                if callback:
                    wx.CallAfter(callback, i)

        return doc.toprettyxml()

    @staticmethod
    def exportMultiBuy(fit):
        export = "%s\n" % (fit.ship.item.name)
        stuff = {}
        sFit = service.Fit.getInstance()
        for module in fit.modules:
            slot = module.slot
            if not slot in stuff:
                stuff[slot] = []
            curr = "%s\n" % module.item.name if module.item else (
            "")
            if module.charge and sFit.serviceFittingOptions["exportCharges"]:
                curr += "%s x%s\n" % (module.charge.name, module.numShots)
            stuff[slot].append(curr)

        for slotType in EFT_SLOT_ORDER:
            data = stuff.get(slotType)
            if data is not None:
                # export += "\n"
                for curr in data:
                    export += curr

        if len(fit.drones) > 0:
            for drone in fit.drones:
                export += "%s x%s\n" % (drone.item.name, drone.amount)

        if len(fit.cargo) > 0:
            for cargo in fit.cargo:
                export += "%s x%s\n" % (cargo.item.name, cargo.amount)

        if len(fit.implants) > 0:
            for implant in fit.implants:
                export += "%s\n" % implant.item.name

        if len(fit.boosters) > 0:
            for booster in fit.boosters:
                export += "%s\n" % booster.item.name

        if len(fit.fighters) > 0:
            for fighter in fit.fighters:
                export += "%s x%s\n" % (fighter.item.name, fighter.amountActive)

        if export[-1] == "\n":
            export = export[:-1]

        return export
