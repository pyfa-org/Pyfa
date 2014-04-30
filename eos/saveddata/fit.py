#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from eos.effectHandlerHelpers import HandledList, HandledModuleList, HandledDroneList, HandledImplantBoosterList, \
HandledProjectedFitList, HandledProjectedModList, HandledProjectedDroneList
from eos.modifiedAttributeDict import ModifiedAttributeDict
from sqlalchemy.orm import validates, reconstructor
from itertools import chain
from eos import capSim
from copy import deepcopy
from math import sqrt, log, asinh
from eos.types import Drone, Ship, Character, State, Slot, Module, Implant, Booster, Skill
from eos.saveddata.module import State
import re
import xml.dom
import time

try:
    from collections import OrderedDict
except ImportError:
    from gui.utils.compat import OrderedDict

class Fit(object):
    """Represents a fitting, with modules, ship, implants, etc."""
    EXTRA_ATTRIBUTES = {"armorRepair": 0,
                        "hullRepair": 0,
                        "shieldRepair": 0,
                        "maxActiveDrones": 0,
                        "maxTargetsLockedFromSkills": 2,
                        "droneControlRange": 20000,
                        "cloaked": False,
                        "siege": False}

    PEAK_RECHARGE = 0.25

    def __init__(self):
        self.__modules = HandledModuleList()
        self.__drones = HandledDroneList()
        self.__implants = HandledImplantBoosterList()
        self.__boosters = HandledImplantBoosterList()
        self.__projectedFits = HandledProjectedFitList()
        self.__projectedModules = HandledProjectedModList()
        self.__projectedDrones = HandledProjectedDroneList()
        self.__character = None
        self.__owner = None
        self.shipID = None
        self.projected = False
        self.name = ""
        self.fleet = None
        self.boostsFits = set()
        self.gangBoosts = None
        self.timestamp = time.time()
        self.build()

    @classmethod
    def importAuto(cls, string, sourceFileName=None):
        # Get first line and strip space symbols of it
        # to avoid possible detection errors
        firstLine = re.split("[\n\r]+", string, maxsplit=1)[0]
        firstLine = firstLine.strip()

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
        elif re.match("\[.*\]", firstLine) and sourceFileName is not None:
            shipName = sourceFileName.rsplit('.')[0]
            return "EFT Config", cls.importEftCfg(shipName, string)
        # If no file is specified and there's comma between brackets,
        # consider that we have [ship, setup name] and detect like eft export format
        elif re.match("\[.*,.*\]", firstLine):
            return "EFT", (cls.importEft(string),)
        # Use DNA format for all other cases
        else:
            return "DNA", (cls.importDna(string),)

    @classmethod
    def importCrest(cls, info):
        from eos import db
        import urllib2
        import json

        try:
            response = urllib2.urlopen("https://public-crest.eveonline.com/killmails/%s/%s/" % info)
        except:
            return

        kill = (json.loads(response.read()))['victim']

        fit = Fit()
        fit.ship = Ship(db.getItem(kill['shipType']['name']))
        fit.name = "CREST: %s's %s" % (kill['character']['name'], kill['shipType']['name'])

        # sort based on flag to get proper rack position
        items  = sorted(kill['items'], key=lambda k: k['flag'])

        # We create a relation between module flag and module position on fit at time of append:
        # this allows us to know which module to apply charges to if need be (see below)
        flagMap = {}

        # Charges may show up before or after the module. We process modules first,
        # storing any charges that are fitted in a dict and noting their flag (module).
        charges = {}

        for mod in items:
            if mod['flag'] == 5: # throw out cargo
                continue

            item = db.getItem(mod['itemType']['name'], eager="group.category")

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

    @classmethod
    def importDna(cls, string):
        from eos import db
        info = string.split(":")
        f = Fit()
        f.ship = Ship(db.getItem(int(info[0])))
        f.name = "{0} - DNA Imported".format(f.ship.item.name)
        for itemInfo in info[1:]:
            if itemInfo:
                itemID, amount = itemInfo.split(";")
                item = db.getItem(int(itemID), eager="group.category")

                if item.category.name == "Drone":
                    d = Drone(item)
                    d.amount = int(amount)
                    f.drones.append(d)
                elif item.category.name == "Charge":
                    for i in xrange(int(amount)):
                        for mod in f.modules:
                            if (mod.isValidCharge(item) and mod.charge == None):
                                mod.charge = item
                                break;
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

    @classmethod
    def importEft(cls, eftString):
        from eos import db
        offineSuffix = " /OFFLINE"
        fit = cls()
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
            fit.ship = Ship(db.getItem(shipType))
            fit.name = fitName
        except:
            return
        droneMap = {}
        for i in range(1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            setOffline = line.endswith(offineSuffix)
            if setOffline == True:
                line = line[:len(line) - len(offineSuffix)]
            modAmmo = line.split(",")
            modDrone = modAmmo[0].split(" x")
            if len(modAmmo) == 2: ammoName = modAmmo[1].strip()
            else: ammoName = None
            modName = modDrone[0].strip()
            if len(modDrone) == 2: droneAmount = modDrone[1].strip()
            else: droneAmount = None
            try:
                item = db.getItem(modName, eager="group.category")
            except:
                try:
                    item = db.getItem(modAmmo[0], eager="group.category")
                except:
                    continue

            if item.category.name == "Drone":
                droneAmount = int(droneAmount) if droneAmount is not None else 1
                if not modName in droneMap:
                    droneMap[modName] = 0
                droneMap[modName] += droneAmount
            elif item.category.name == "Implant":
                fit.implants.append(Implant(item))
            else:
                try:
                    m = Module(item)
                except ValueError:
                    continue
                if ammoName:
                    try:
                        m.charge = db.getItem(ammoName)
                    except:
                        pass

                if setOffline == True and m.isValidState(State.OFFLINE):
                    m.state = State.OFFLINE
                elif m.isValidState(State.ACTIVE):
                    m.state = State.ACTIVE

                fit.modules.append(m)

        for droneName in droneMap:
            d = Drone(db.getItem(droneName))
            d.amount = droneMap[droneName]
            fit.drones.append(d)

        return fit

    @classmethod
    def importEftCfg(cls, shipname, contents):
        """Handle import from EFT config store file"""
        # Check if we have such ship in database, bail if we don't
        from eos import db
        try:
            db.getItem(shipname)
        except:
            return
        # If client didn't take care of encoding file contents into Unicode,
        # do it using fallback encoding ourselves
        if isinstance(contents, str):
            contents = unicode(contents, "cp1252")
        # List for fits
        fits = []
        # List for starting line numbers for each fit
        fitIndices = []
        # Separate string into lines
        lines = re.split('[\n\r]+', contents)
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
                f.ship = Ship(db.getItem(shipname))
                for i in range(1, len(fitLines)):
                    line = fitLines[i]
                    # Parse line into some data we will need
                    misc = re.match("(Drones|Implant|Booster)_(Active|Inactive)=(.+)",line)
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
                                droneItem = db.getItem(droneName, eager="group.category")
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
                                implantItem = db.getItem(entityData, eager="group.category")
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
                                boosterItem = db.getItem(entityData, eager="group.category")
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
                    else:
                        withCharge = re.match("(.+),(.+)", line)
                        modName = withCharge.group(1) if withCharge else line
                        chargeName = withCharge.group(2) if withCharge else None
                        # If we can't get module item, skip it
                        try:
                            modItem = db.getItem(modName)
                        except:
                            continue
                        # Create module and activate it if it's activable
                        m = Module(modItem)
                        if m.isValidState(State.ACTIVE):
                            m.state = State.ACTIVE
                        # Add charge to mod if applicable, on any errors just don't add anything
                        if chargeName:
                            try:
                                chargeItem = db.getItem(chargeName, eager="group.category")
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

    @classmethod
    def importXml(cls, text):
        doc = xml.dom.minidom.parseString(text.encode("utf-8"))
        fittings = doc.getElementsByTagName("fittings").item(0)
        fittings = fittings.getElementsByTagName("fitting")
        fits = []
        from eos import db
        for fitting in fittings:
            f = Fit()
            f.name = fitting.getAttribute("name")
            # <localized hint="Maelstrom">Maelstrom</localized>
            shipType = fitting.getElementsByTagName("shipType").item(0).getAttribute("value")
            try:
                f.ship = Ship(db.getItem(shipType))
            except:
                continue
            hardwares = fitting.getElementsByTagName("hardware")
            for hardware in hardwares:
                try:
                    moduleName = hardware.getAttribute("type")
                    try:
                        item = db.getItem(moduleName, eager="group.category")
                    except:
                        continue
                    if item:
                        if item.category.name == "Drone":
                            d = Drone(item)
                            d.amount = int(hardware.getAttribute("qty"))
                            f.drones.append(d)
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

    EXPORT_ORDER_EFT = [Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM]
    def exportEft(self):
        offineSuffix = " /OFFLINE"
        export = "[%s, %s]\n" % (self.ship.item.name, self.name)
        stuff = {}
        for module in self.modules:
            slot = module.slot
            if not slot in stuff: stuff[slot] = []
            curr = module.item.name if module.item else ("[Empty %s slot]" % Slot.getName(slot).capitalize() if slot is not None else "")
            if module.charge:
                curr += ", %s" % module.charge.name
            if module.state == State.OFFLINE:
                curr += offineSuffix
            curr += "\n"
            stuff[slot].append(curr)

        for slotType in self.EXPORT_ORDER_EFT:
            data = stuff.get(slotType)
            if data is not None:
                export += "\n"
                for curr in data:
                    export += curr

        if len(self.drones) > 0:
            export += "\n\n"
            for drone in self.drones:
                export += "%s x%s\n" % (drone.item.name, drone.amount)

        if export[-1] == "\n":
            export = export[:-1]

        return export

    def exportEftImps(self):
        export = self.exportEft()
        if len(self.implants) > 0:
            export += "\n\n\n"
            for implant in self.implants:
                export += "%s\n" % (implant.item.name)

        if export[-1] == "\n":
            export = export[:-1]

        return export

    def exportDna(self):
        dna = str(self.shipID)
        mods = OrderedDict()
        charges = OrderedDict()
        for mod in self.modules:
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

        for drone in self.drones:
            dna += ":{0};{1}".format(drone.itemID, drone.amount)

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
                if not slot in slotNum: slotNum[slot] = 0
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

            for name, qty in charges.items():
                hardware = doc.createElement("hardware")
                hardware.setAttribute("qty", "%d" % qty)
                hardware.setAttribute("slot", "cargo")
                hardware.setAttribute("type", name)
                fitting.appendChild(hardware)

        return doc.toprettyxml()

    @reconstructor
    def init(self):
        self.build()

    def build(self):
        from eos import db
        self.__extraDrains = []
        self.__ehp = None
        self.__weaponDPS = None
        self.__weaponVolley = None
        self.__droneDPS = None
        self.__sustainableTank = None
        self.__effectiveSustainableTank = None
        self.__effectiveTank = None
        self.__calculated = False
        self.__capStable = None
        self.__capState = None
        self.__capUsed = None
        self.__capRecharge = None
        self.__calculatedTargets = []
        self.factorReload = False
        self.fleet = None
        self.boostsFits = set()
        self.gangBoosts = None
        self.extraAttributes = ModifiedAttributeDict(self)
        self.extraAttributes.original = self.EXTRA_ATTRIBUTES
        self.ship = Ship(db.getItem(self.shipID)) if self.shipID is not None else None

    @property
    def damagePattern(self):
        return self.__damagePattern

    @damagePattern.setter
    def damagePattern(self, damagePattern):
        self.__damagePattern = damagePattern
        self.__ehp = None
        self.__effectiveTank = None

    @property
    def character(self):
        return self.__character if self.__character is not None else Character.getAll0()

    @character.setter
    def character(self, char):
        self.__character = char

    @property
    def ship(self):
        return self.__ship

    @ship.setter
    def ship(self, ship):
        self.__ship = ship
        self.shipID = ship.item.ID if ship is not None else None

    @property
    def drones(self):
        return self.__drones

    @property
    def modules(self):
        return self.__modules

    @property
    def implants(self):
        return self.__implants

    @property
    def boosters(self):
        return self.__boosters

    @property
    def projectedModules(self):
        return self.__projectedModules

    @property
    def projectedFits(self):
        return self.__projectedFits

    @property
    def projectedDrones(self):
        return self.__projectedDrones

    @property
    def weaponDPS(self):
        if self.__weaponDPS is None:
            self.calculateWeaponStats()

        return self.__weaponDPS

    @property
    def weaponVolley(self):
        if self.__weaponVolley is None:
            self.calculateWeaponStats()

        return self.__weaponVolley

    @property
    def droneDPS(self):
        if self.__droneDPS is None:
            self.calculateWeaponStats()

        return self.__droneDPS

    @property
    def totalDPS(self):
        return self.droneDPS + self.weaponDPS

    @property
    def maxTargets(self):
        return min(self.extraAttributes["maxTargetsLockedFromSkills"], self.ship.getModifiedItemAttr("maxLockedTargets"))

    @property
    def maxTargetRange(self):
        return min(self.ship.getModifiedItemAttr("maxTargetRange"), 250000)

    @property
    def scanStrength(self):
        return max([self.ship.getModifiedItemAttr("scan%sStrength" % scanType)
                    for scanType in ("Magnetometric", "Ladar", "Radar", "Gravimetric")])

    @property
    def scanType(self):
        maxStr = -1
        type = None
        for scanType in ("Magnetometric", "Ladar", "Radar", "Gravimetric"):
            currStr = self.ship.getModifiedItemAttr("scan%sStrength" % scanType)
            if currStr > maxStr:
                maxStr = currStr
                type = scanType
            elif currStr == maxStr:
                type = "Multispectral"

        return type

    @property
    def alignTime(self):
        agility = self.ship.getModifiedItemAttr("agility")
        mass = self.ship.getModifiedItemAttr("mass")

        return -log(0.25) * agility * mass / 1000000

    @property
    def appliedImplants(self):
        implantsBySlot = {}
        if self.character:
            for implant in self.character.implants:
                implantsBySlot[implant.slot] = implant

        for implant in self.implants:
            implantsBySlot[implant.slot] = implant

        return implantsBySlot.values()

    @validates("ID", "ownerID", "shipID")
    def validator(self, key, val):
        map = {"ID": lambda val: isinstance(val, int),
               "ownerID" : lambda val: isinstance(val, int),
               "shipID" : lambda val: isinstance(val, int) or val is None}

        if map[key](val) == False: raise ValueError(str(val) + " is not a valid value for " + key)
        else: return val

    def clear(self):
        self.__effectiveTank = None
        self.__weaponDPS = None
        self.__weaponVolley = None
        self.__effectiveSustainableTank = None
        self.__sustainableTank = None
        self.__droneDPS = None
        self.__ehp = None
        self.__calculated = False
        self.__capStable = None
        self.__capState = None
        self.__capUsed = None
        self.__capRecharge = None
        del self.__calculatedTargets[:]
        del self.__extraDrains[:]

        if self.ship is not None: self.ship.clear()
        c = chain(self.modules, self.drones, self.boosters, self.implants, self.projectedDrones, self.projectedModules, self.projectedFits, (self.character, self.extraAttributes))
        for stuff in c:
            if stuff is not None and stuff != self: stuff.clear()

    #Methods to register and get the thing currently affecting the fit,
    #so we can correctly map "Affected By"
    def register(self, currModifier):
        self.__modifier = currModifier
        if hasattr(currModifier, "itemModifiedAttributes"):
            currModifier.itemModifiedAttributes.fit = self
        if hasattr(currModifier, "chargeModifiedAttributes"):
            currModifier.chargeModifiedAttributes.fit = self

    def getModifier(self):
        return self.__modifier

    def calculateModifiedAttributes(self, targetFit=None, withBoosters=False, dirtyStorage=None):
        refreshBoosts = False
        if withBoosters is True:
            refreshBoosts = True
        if dirtyStorage is not None and self.ID in dirtyStorage:
            refreshBoosts = True
        if dirtyStorage is not None:
            dirtyStorage.update(self.boostsFits)
        if self.fleet is not None and refreshBoosts is True:
            self.gangBoosts = self.fleet.recalculateLinear(withBoosters=withBoosters, dirtyStorage=dirtyStorage)
        elif self.fleet is None:
            self.gangBoosts = None
        if dirtyStorage is not None:
            try:
                dirtyStorage.remove(self.ID)
            except KeyError:
                pass
        # If we're not explicitly asked to project fit onto something,
        # set self as target fit
        if targetFit is None:
            targetFit = self
            forceProjected = False
        # Else, we're checking all target projectee fits
        elif targetFit not in self.__calculatedTargets:
            self.__calculatedTargets.append(targetFit)
            targetFit.calculateModifiedAttributes(dirtyStorage=dirtyStorage)
            forceProjected = True
        # Or do nothing if target fit is calculated
        else:
            return

        # If fit is calculated and we have nothing to do here, get out
        if self.__calculated == True and forceProjected == False:
            return

        # Mark fit as calculated
        self.__calculated = True

        # There's a few things to keep in mind here
        # 1: Early effects first, then regular ones, then late ones, regardless of anything else
        # 2: Some effects aren't implemented
        # 3: Some effects are implemented poorly and will just explode on us
        # 4: Errors should be handled gracefully and preferably without crashing unless serious
        for runTime in ("early", "normal", "late"):
            # Build a little chain of stuff
            # Avoid adding projected drones and modules when fit is projected onto self
            # TODO: remove this workaround when proper self-projection using virtual duplicate fits is implemented
            if targetFit == self and forceProjected is True:
                c = chain((self.character, self.ship), self.drones, self.boosters, self.appliedImplants, self.modules)
            else:
                c = chain((self.character, self.ship), self.drones, self.boosters, self.appliedImplants, self.modules,
                          self.projectedDrones, self.projectedModules)

            for item in c:
                # Registering the item about to affect the fit allows us to track "Affected By" relations correctly
                if item is not None:
                    self.register(item)
                    item.calculateModifiedAttributes(self, runTime, False)
                    if forceProjected is True:
                        targetFit.register(item)
                        item.calculateModifiedAttributes(targetFit, runTime, True)
            if self.gangBoosts is not None:
                #print self.gangBoosts
                contextMap = {Skill: "skill",
                              Ship: "ship",
                              Module: "module",
                              Implant: "implant"}
                for name, info in self.gangBoosts.iteritems():
                    # Unpack all data required to run effect properly
                    effect, thing = info[1]
                    if effect.runTime == runTime:
                        context = ("gang", contextMap[type(thing)])
                        if isinstance(thing, Module):
                            if effect.isType("offline") or (effect.isType("passive") and thing.state >= State.ONLINE) or \
                            (effect.isType("active") and thing.state >= State.ACTIVE):
                                # Run effect, and get proper bonuses applied
                                try:
                                    effect.handler(targetFit, thing, context)
                                except:
                                    pass
                        else:
                            # Run effect, and get proper bonuses applied
                            try:
                                effect.handler(targetFit, thing, context)
                            except:
                                pass
        for fit in self.projectedFits:
            fit.calculateModifiedAttributes(self, dirtyStorage=dirtyStorage)

    def fill(self):
        """
        Fill this fit's module slots with enough dummy slots so that all slots are used.
        This is mostly for making the life of gui's easier.
        GUI's can call fill() and then stop caring about empty slots completely.
        """
        if self.ship is None:
            return

        for slotType in (Slot.LOW, Slot.MED, Slot.HIGH, Slot.RIG, Slot.SUBSYSTEM):
            amount = self.getSlotsFree(slotType, True)
            if amount > 0:
                for _ in xrange(int(amount)):
                    self.modules.append(Module.buildEmpty(slotType))

            if amount < 0:
                #Look for any dummies of that type to remove
                toRemove = []
                for mod in self.modules:
                    if mod.isEmpty and mod.slot == slotType:
                        toRemove.append(mod)
                        amount += 1
                        if amount == 0:
                            break
                for mod in toRemove:
                    self.modules.remove(mod)

    def unfill(self):
        for i in xrange(len(self.modules) - 1, -1, -1):
            mod = self.modules[i]
            if mod.isEmpty:
                del self.modules[i]

    def getItemAttrSum(self, dict, attr):
        amount = 0
        for mod in dict:
            add = mod.getModifiedItemAttr(attr)
            if add is not None:
                amount += add

        return amount

    def getItemAttrOnlineSum(self, dict, attr):
        amount = 0
        for mod in dict:
            add = mod.getModifiedItemAttr(attr) if mod.state >= State.ONLINE else None
            if add is not None:
                amount += add

        return amount

    def getHardpointsUsed(self, type):
        amount = 0
        for mod in self.modules:
            if mod.hardpoint is type and not mod.isEmpty:
                amount += 1

        return amount

    def getSlotsUsed(self, type, countDummies=False):
        amount = 0
        for mod in self.modules:
            if mod.slot is type and (not mod.isEmpty or countDummies):
                amount += 1

        return amount

    def getSlotsFree(self, type, countDummies=False):
        slots = {Slot.LOW: "lowSlots",
                 Slot.MED: "medSlots",
                 Slot.HIGH: "hiSlots",
                 Slot.RIG: "rigSlots",
                 Slot.SUBSYSTEM: "maxSubSystems"}

        slotsUsed = self.getSlotsUsed(type, countDummies)
        totalSlots = self.ship.getModifiedItemAttr(slots[type]) or 0
        return int(totalSlots - slotsUsed)

    @property
    def calibrationUsed(self):
        return self.getItemAttrSum(self.modules, 'upgradeCost')

    @property
    def pgUsed(self):
        return self.getItemAttrOnlineSum(self.modules, "power")

    @property
    def cpuUsed(self):
        return self.getItemAttrOnlineSum(self.modules, "cpu")

    @property
    def droneBandwidthUsed(self):
        amount = 0
        for d in self.drones:
            amount += d.getModifiedItemAttr("droneBandwidthUsed") * d.amountActive

        return amount

    @property
    def droneBayUsed(self):
        amount = 0
        for d in self.drones:
            amount += d.item.volume * d.amount

        return amount

    @property
    def activeDrones(self):
        amount = 0
        for d in self.drones:
            amount +=d.amountActive

        return amount

    # Expresses how difficult a target is to probe down with scan probes
    # If this is <1.08, the ship is unproabeable
    @property
    def probeSize(self):
        sigRad = self.ship.getModifiedItemAttr("signatureRadius")
        sensorStr = float(self.scanStrength)
        probeSize = sigRad / sensorStr if sensorStr != 0 else None
        # http://www.eveonline.com/ingameboard.asp?a=topic&threadID=1532170&page=2#42
        if probeSize is not None:
            # http://forum.eve-ru.com/index.php?showtopic=74195&view=findpost&p=1333691
            # http://forum.eve-ru.com/index.php?showtopic=74195&view=findpost&p=1333763
            # Tests by tester128 and several conclusions by me, prove that cap is in range
            # from 1.1 to 1.12, we're picking average value
            probeSize = max(probeSize, 1.11)
        return probeSize

    @property
    def warpSpeed(self):
        base = self.ship.getModifiedItemAttr("baseWarpSpeed") or 1
        multiplier = self.ship.getModifiedItemAttr("warpSpeedMultiplier") or 1
        return base * multiplier

    @property
    def maxWarpDistance(self):
        capacity = self.ship.getModifiedItemAttr("capacitorCapacity")
        mass = self.ship.getModifiedItemAttr("mass")
        warpCapNeed = self.ship.getModifiedItemAttr("warpCapacitorNeed")
        return capacity / (mass * warpCapNeed)

    @property
    def capStable(self):
        if self.__capStable is None:
            self.simulateCap()

        return self.__capStable

    @property
    def capState(self):
        """
        If the cap is stable, the capacitor state is the % at which it is stable.
        If the cap is unstable, this is the amount of time before it runs out
        """
        if self.__capState is None:
            self.simulateCap()

        return self.__capState

    @property
    def capUsed(self):
        if self.__capUsed is None:
            self.simulateCap()

        return self.__capUsed

    @property
    def capRecharge(self):
        if self.__capRecharge is None:
            self.simulateCap()

        return self.__capRecharge


    @property
    def sustainableTank(self):
        if self.__sustainableTank is None:
            self.calculateSustainableTank()

        return self.__sustainableTank

    def calculateSustainableTank(self, effective=True):
        if self.__sustainableTank is None:
            if self.capStable:
                sustainable = {}
                sustainable["armorRepair"] = self.extraAttributes["armorRepair"]
                sustainable["shieldRepair"] = self.extraAttributes["shieldRepair"]
                sustainable["hullRepair"] = self.extraAttributes["hullRepair"]
            else:
                sustainable = {}

                repairers = []
                #Map a repairer type to the attribute it uses
                groupAttrMap = {"Armor Repair Unit": "armorDamageAmount",
                     "Fueled Armor Repairer": "armorDamageAmount",
                     "Hull Repair Unit": "structureDamageAmount",
                     "Shield Booster": "shieldBonus",
                     "Fueled Shield Booster": "shieldBonus",
                     "Remote Armor Repairer": "armorDamageAmount",
                     "Remote Shield Booster": "shieldBonus"}
                #Map repairer type to attribute
                groupStoreMap = {"Armor Repair Unit": "armorRepair",
                                 "Hull Repair Unit": "hullRepair",
                                 "Shield Booster": "shieldRepair",
                                 "Fueled Shield Booster": "shieldRepair",
                                 "Remote Armor Repairer": "armorRepair",
                                 "Remote Shield Booster": "shieldRepair",
                                 "Fueled Armor Repairer": "armorRepair",}

                capUsed = self.capUsed
                for attr in ("shieldRepair", "armorRepair", "hullRepair"):
                    sustainable[attr] = self.extraAttributes[attr]
                    dict = self.extraAttributes.getAfflictions(attr)
                    if self in dict:
                        for mod, _, amount in dict[self]:
                            if mod.projected is False:
                                usesCap = True
                                try:
                                    if mod.capUse:
                                        capUsed -= mod.capUse
                                    else:
                                        usesCap = False
                                except AttributeError:
                                    usesCap = False
                                # Modules which do not use cap are not penalized based on cap use
                                if usesCap:
                                    cycleTime = mod.getModifiedItemAttr("duration")
                                    amount = mod.getModifiedItemAttr(groupAttrMap[mod.item.group.name])
                                    sustainable[attr] -= amount / (cycleTime / 1000.0)
                                    repairers.append(mod)


                #Sort repairers by efficiency. We want to use the most efficient repairers first
                repairers.sort(key=lambda mod: mod.getModifiedItemAttr(groupAttrMap[mod.item.group.name]) / mod.getModifiedItemAttr("capacitorNeed"), reverse = True)

                #Loop through every module until we're above peak recharge
                #Most efficient first, as we sorted earlier.
                #calculate how much the repper can rep stability & add to total
                totalPeakRecharge = self.capRecharge
                for mod in repairers:
                    if capUsed > totalPeakRecharge: break
                    cycleTime = mod.cycleTime
                    capPerSec = mod.capUse
                    if capPerSec is not None and cycleTime is not None:
                        #Check how much this repper can work
                        sustainability = min(1, (totalPeakRecharge - capUsed) / capPerSec)

                        #Add the sustainable amount
                        amount = mod.getModifiedItemAttr(groupAttrMap[mod.item.group.name])
                        sustainable[groupStoreMap[mod.item.group.name]] += sustainability * (amount / (cycleTime / 1000.0))
                        capUsed += capPerSec

            sustainable["passiveShield"] = self.calculateShieldRecharge()
            self.__sustainableTank = sustainable

        return self.__sustainableTank

    def calculateCapRecharge(self, percent = PEAK_RECHARGE):
        capacity = self.ship.getModifiedItemAttr("capacitorCapacity")
        rechargeRate = self.ship.getModifiedItemAttr("rechargeRate") / 1000.0
        return 10 / rechargeRate * sqrt(percent) * (1 - sqrt(percent)) * capacity

    def calculateShieldRecharge(self, percent = PEAK_RECHARGE):
        capacity = self.ship.getModifiedItemAttr("shieldCapacity")
        rechargeRate = self.ship.getModifiedItemAttr("shieldRechargeRate") / 1000.0
        return 10 / rechargeRate * sqrt(percent) * (1 - sqrt(percent)) * capacity

    def addDrain(self, cycleTime, capNeed, clipSize=0):
        self.__extraDrains.append((cycleTime, capNeed, clipSize))

    def removeDrain(self, i):
        del self.__extraDrains[i]

    def iterDrains(self):
        return self.__extraDrains.__iter__()

    def __generateDrain(self):
        drains = []
        capUsed = 0
        capAdded = 0
        for mod in self.modules:
            if mod.state >= State.ACTIVE:
                    cycleTime = mod.rawCycleTime or 0
                    reactivationTime = mod.getModifiedItemAttr("moduleReactivationDelay") or 0
                    fullCycleTime = cycleTime + reactivationTime
                    if fullCycleTime > 0:
                        capNeed = mod.capUse
                        if capNeed > 0:
                            capUsed += capNeed
                        else:
                            capAdded -= capNeed

                        drains.append((int(fullCycleTime), mod.getModifiedItemAttr("capacitorNeed") or 0, mod.numShots or 0))

        for fullCycleTime, capNeed, clipSize in self.iterDrains():
            drains.append((int(fullCycleTime), capNeed, clipSize))
            if capNeed > 0:
                capUsed += capNeed / (fullCycleTime / 1000.0)
            else:
                capAdded += -capNeed / (fullCycleTime / 1000.0)

        return drains, capUsed, capAdded

    def simulateCap(self):
        drains, self.__capUsed, self.__capRecharge = self.__generateDrain()
        self.__capRecharge += self.calculateCapRecharge()
        if len(drains) > 0:
            sim = capSim.CapSimulator()
            sim.init(drains)
            sim.capacitorCapacity = self.ship.getModifiedItemAttr("capacitorCapacity")
            sim.capacitorRecharge = self.ship.getModifiedItemAttr("rechargeRate")
            sim.stagger = True
            sim.scale = False
            sim.t_max = 6 * 60 * 60 * 1000
            sim.reload = self.factorReload
            sim.run()

            capState = (sim.cap_stable_low + sim.cap_stable_high) / (2 * sim.capacitorCapacity)
            self.__capStable = capState > 0
            self.__capState = min(100, capState * 100) if self.__capStable else sim.t / 1000.0
        else:
            self.__capStable = True
            self.__capState = 100

    @property
    def hp(self):
        hp = {}
        for (type, attr) in (('shield', 'shieldCapacity'), ('armor', 'armorHP'), ('hull', 'hp')):
            hp[type] = self.ship.getModifiedItemAttr(attr)

        return hp

    @property
    def ehp(self):
        if self.__ehp is None:
            if self.damagePattern is None:
                ehp = self.hp
            else:
                ehp = self.damagePattern.calculateEhp(self)
            self.__ehp = ehp

        return self.__ehp

    @property
    def tank(self):
        hps = {"passiveShield" : self.calculateShieldRecharge()}
        for type in ("shield", "armor", "hull"):
            hps["%sRepair" % type] = self.extraAttributes["%sRepair" % type]

        return hps

    @property
    def effectiveTank(self):
        if self.__effectiveTank is None:
            if self.damagePattern is None:
                ehps = self.tank
            else:
                ehps = self.damagePattern.calculateEffectiveTank(self, self.extraAttributes)

            self.__effectiveTank = ehps

        return self.__effectiveTank

    @property
    def effectiveSustainableTank(self):
        if self.__effectiveSustainableTank is None:
            if self.damagePattern is None:
                eshps = self.sustainableTank
            else:
                eshps = self.damagePattern.calculateEffectiveTank(self, self.sustainableTank)

            self.__effectiveSustainableTank = eshps

        return self.__effectiveSustainableTank


    def calculateLockTime(self, radius):
        scanRes = self.ship.getModifiedItemAttr("scanResolution")
        if scanRes is not None and scanRes > 0:
            # Yes, this function returns time in seconds, not miliseconds.
            # 40,000 is indeed the correct constant here.
            return min(40000 / scanRes / asinh(radius)**2, 30*60)
        else:
            return self.ship.getModifiedItemAttr("scanSpeed") / 1000.0

    def calculateWeaponStats(self):
        weaponDPS = 0
        droneDPS = 0
        weaponVolley = 0

        for mod in self.modules:
            dps, volley = mod.damageStats
            weaponDPS += dps
            weaponVolley += volley

        for drone in self.drones:
            droneDPS += drone.dps

        self.__weaponDPS = weaponDPS
        self.__weaponVolley = weaponVolley
        self.__droneDPS = droneDPS

    @property
    def fits(self):
        for mod in self.modules:
            if not mod.fits(self):
                return False

        return True

    def __deepcopy__(self, memo):
        copy = Fit()
        #Character and owner are not copied
        copy.character = self.__character
        copy.owner = self.owner
        copy.ship = deepcopy(self.ship, memo)
        copy.name = "%s copy" % self.name
        copy.damagePattern = self.damagePattern

        toCopy = ("modules", "drones", "implants", "boosters", "projectedModules", "projectedDrones")
        for name in toCopy:
            orig = getattr(self, name)
            c = getattr(copy, name)
            for i in orig:
                c.append(deepcopy(i, memo))

        for fit in self.projectedFits:
            copy.projectedFits.append(fit)

        return copy
