#===============================================================================
# Copyright (C) 2010 Diego Duclos
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
import xml.dom
import urllib2
import json

from eos.types import State, Slot, Module, Cargo, Fit, Ship, Drone, Implant, Booster
import service

try:
    from collections import OrderedDict
except ImportError:
    from gui.utils.compat import OrderedDict


class Port(object):
    """Service which houses all import/export format functions"""

    @classmethod
    def importAuto(cls, string, sourceFileName=None, activeFit=None):
        # Get first line and strip space symbols of it to avoid possible detection errors
        firstLine = re.split("[\n\r]+", string.strip(), maxsplit=1)[0]
        firstLine = firstLine.strip()

        # If string is from in-game copy of fitting window
        # We match " power" instead of "High power" in case a fit has no high modules
        if " power" in firstLine and activeFit is not None:
            return "FIT", (cls.importFittingWindow(string, activeFit),)

        # If we have "<url=fitting", fit is coming from eve chat
        # Gather data and send to DNA
        chatDna = re.search("<url=fitting:(.*::)>.*</url>", firstLine)
        if chatDna:
            return "DNA", (cls.importDna(chatDna.group(1)),)

        # If we have a CREST kill link
        killLink = re.search("http://public-crest.eveonline.com/killmails/(.*)/", firstLine)
        if killLink:
            return "CREST", (cls.importCrest(tuple(killLink.group(1).split("/"))),)

        # If we have "<url=killReport", fit is killmail from eve chat
        killReport = re.search("<url=killReport:(.*)>.*</url>", firstLine)
        if killReport:
            return "CREST", (cls.importCrest(tuple(killReport.group(1).split(":"))),)

        # If XML-style start of tag encountered, detect as XML
        if re.match("<", firstLine):
            return "XML", cls.importXml(string)

        # If we've got source file name which is used to describe ship name
        # and first line contains something like [setup name], detect as eft config file
        if re.match("\[.*\]", firstLine) and sourceFileName is not None:
            shipName = sourceFileName.rsplit('.')[0]
            return "EFT Config", cls.importEftCfg(shipName, string)

        # If no file is specified and there's comma between brackets,
        # consider that we have [ship, setup name] and detect like eft export format
        if re.match("\[.*,.*\]", firstLine):
            return "EFT", (cls.importEft(string),)

        # Use DNA format for all other cases
        return "DNA", (cls.importDna(string),)

    @staticmethod
    def importFittingWindow(string, activeFit):
        sMkt = service.Market.getInstance()
        sFit = service.Fit.getInstance()

        activeFit = sFit.getFit(activeFit)

        # if the current fit has mods, do not mess with it. Instead, make new fit
        if activeFit.modCount > 0:
            fit = Fit()
            fit.ship = Ship(sMkt.getItem(activeFit.ship.item.ID))
            fit.name = "%s (copy)" % activeFit.name
        else:
            fit = activeFit
        lines = re.split('[\n\r]+', string)

        droneMap = {}
        cargoMap = {}
        modules = []

        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            try:
                amount, modName = line.split("x ")
                amount = int(amount)
                item = sMkt.getItem(modName, eager="group.category")
            except:
                # if no data can be found (old names)
                continue

            if item.category.name == "Drone":
                if not modName in droneMap:
                    droneMap[modName] = 0
                droneMap[modName] += amount
            elif item.category.name == "Charge":
                if not modName in cargoMap:
                    cargoMap[modName] = 0
                cargoMap[modName] += amount
            else:
                for _ in xrange(amount):
                    try:
                        m = Module(item)
                    except ValueError:
                        continue
                    # If we are importing T3 ship, we must apply subsystems first, then
                    # calcModAttr() to get the ship slots
                    if m.slot == Slot.SUBSYSTEM and m.fits(fit):
                        fit.modules.append(m)
                    else:
                        modules.append(m)

        fit.clear()
        fit.calculateModifiedAttributes()

        for m in modules:
            # we check to see if module fits as a basic sanity check
            # if it doesn't then the imported fit is most likely invalid
            # (ie: user tried to import Legion fit to a Rifter)
            if m.fits(fit):
                fit.modules.append(m)
                if m.isValidState(State.ACTIVE):
                    m.state = State.ACTIVE
                m.owner = fit  # not sure why this is required when it's not for other import methods, but whatever
            else:
                return

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
    def importCrest(info):
        sMkt = service.Market.getInstance()
        try:
            # @todo: proxy
            response = urllib2.urlopen("https://public-crest.eveonline.com/killmails/%s/%s/" % info)
        except:
            return

        kill = (json.loads(response.read()))['victim']

        fit = Fit()
        fit.ship = Ship(sMkt.getItem(kill['shipType']['name']))
        fit.name = "CREST: %s's %s" % (kill['character']['name'], kill['shipType']['name'])

        # sort based on flag to get proper rack position
        items = sorted(kill['items'], key=lambda k: k['flag'])

        # We create a relation between module flag and module position on fit at time of append:
        # this allows us to know which module to apply charges to if need be (see below)
        flagMap = {}

        # Charges may show up before or after the module. We process modules first,
        # storing any charges that are fitted in a dict and noting their flag (module).
        charges = {}

        for mod in items:
            if mod['flag'] == 5:  # throw out cargo
                continue

            item = sMkt.getItem(mod['itemType']['name'], eager="group.category")

            if item.category.name == "Drone":
                d = Drone(item)
                d.amount = mod['quantityDropped'] if 'quantityDropped' in mod else mod['quantityDestroyed']
                fit.drones.append(d)
            elif item.category.name == "Charge":
                charges[mod['flag']] = item
            else:
                m = Module(item)
                if m.isValidState(State.ACTIVE):
                    m.state = State.ACTIVE
                fit.modules.append(m)
                flagMap[mod['flag']] = fit.modules.index(m)

        for flag, item in charges.items():
            # we do not need to verify valid charge as it comes directly from CCP
            fit.modules[flagMap[flag]].charge = item

        return fit

    @staticmethod
    def importDna(string):
        sMkt = service.Market.getInstance()
        info = string.split(":")

        f = Fit()
        f.ship = Ship(sMkt.getItem(int(info[0])))
        f.name = "{0} - DNA Imported".format(f.ship.item.name)

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
                            f.modules.append(m)
                        except:
                            pass
                        if m.isValidState(State.ACTIVE):
                            m.state = State.ACTIVE

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
            else:
                try:
                    m = Module(item)
                except ValueError:
                    continue
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
    def importEftCfg(shipname, contents):
        """Handle import from EFT config store file"""

        # Check if we have such ship in database, bail if we don't
        sMkt = service.Market.getInstance()
        try:
            sMkt.getItem(shipname)
        except:
            return

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

                        # Create module and activate it if it's activable
                        m = Module(modItem)
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
                        f.modules.append(m)
                # Append fit to list of fits
                fits.append(f)
            # Skip fit silently if we get an exception
            except Exception:
                pass

        return fits

    @staticmethod
    def importXml(text):
        sMkt = service.Market.getInstance()

        doc = xml.dom.minidom.parseString(text.encode("utf-8"))
        fittings = doc.getElementsByTagName("fittings").item(0)
        fittings = fittings.getElementsByTagName("fitting")
        fits = []
        for fitting in fittings:
            f = Fit()
            f.name = fitting.getAttribute("name")
            # <localized hint="Maelstrom">Maelstrom</localized>
            shipType = fitting.getElementsByTagName("shipType").item(0).getAttribute("value")
            try:
                f.ship = Ship(sMkt.getItem(shipType))
            except:
                continue
            hardwares = fitting.getElementsByTagName("hardware")
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
                            if m.isValidState(State.ACTIVE):
                                m.state = State.ACTIVE

                            f.modules.append(m)
                except KeyboardInterrupt:
                    continue
            fits.append(f)

        return fits

    @staticmethod
    def exportEft(fitID):
        sFit = service.Fit.getInstance()
        fit = sFit.getFit(fitID)

        offineSuffix = " /OFFLINE"
        export = "[%s, %s]\n" % (fit.ship.item.name, fit.name)
        stuff = {}
        for module in fit.modules:
            slot = module.slot
            if not slot in stuff:
                stuff[slot] = []
            curr = module.item.name if module.item else ("[Empty %s slot]" % Slot.getName(slot).capitalize() if slot is not None else "")
            if module.charge:
                curr += ", %s" % module.charge.name
            if module.state == State.OFFLINE:
                curr += offineSuffix
            curr += "\n"
            stuff[slot].append(curr)

        for slotType in [Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM]:
            data = stuff.get(slotType)
            if data is not None:
                export += "\n"
                for curr in data:
                    export += curr

        if len(fit.drones) > 0:
            export += "\n\n"
            for drone in fit.drones:
                export += "%s x%s\n" % (drone.item.name, drone.amount)
        if len(fit.cargo) > 0:
            for cargo in fit.cargo:
                export += "%s x%s\n" % (cargo.item.name, cargo.amount)

        if export[-1] == "\n":
            export = export[:-1]

        return export

    @classmethod
    def exportEftImps(cls, fitID):
        export = cls.exportEft(fitID)

        sFit = service.Fit.getInstance()
        fit = sFit.getFit(fitID)

        if len(fit.implants) > 0:
            export += "\n\n\n"
            for implant in fit.implants:
                export += "%s\n" % implant.item.name

        if export[-1] == "\n":
            export = export[:-1]

        return export

    @staticmethod
    def exportDna(fitID):
        sFit = service.Fit.getInstance()
        fit = sFit.getFit(fitID)

        dna = str(fit.shipID)
        mods = OrderedDict()
        charges = OrderedDict()
        for mod in fit.modules:
            if not mod.isEmpty:
                if not mod.itemID in mods:
                    mods[mod.itemID] = 0
                mods[mod.itemID] += 1

                if mod.charge:
                    if not mod.chargeID in charges:
                        charges[mod.chargeID] = 0
                    # `or 1` because some charges (ie scripts) are without qty
                    charges[mod.chargeID] += mod.numShots or 1

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
    def exportXml(cls, *fits):
        doc = xml.dom.minidom.Document()
        fittings = doc.createElement("fittings")
        doc.appendChild(fittings)
        for fit in fits:
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

                if module.charge:
                    if not module.charge.name in charges:
                        charges[module.charge.name] = 0
                    # `or 1` because some charges (ie scripts) are without qty
                    charges[module.charge.name] += module.numShots or 1

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

        return doc.toprettyxml()
