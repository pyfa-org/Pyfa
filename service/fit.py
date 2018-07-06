# ===============================================================================
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
# ===============================================================================

import copy
from logbook import Logger
from time import time
import datetime

import eos.db
from eos.saveddata.booster import Booster as es_Booster
from eos.saveddata.cargo import Cargo as es_Cargo
from eos.saveddata.character import Character as saveddata_Character
from eos.saveddata.citadel import Citadel as es_Citadel
from eos.saveddata.damagePattern import DamagePattern as es_DamagePattern
from eos.saveddata.drone import Drone as es_Drone
from eos.saveddata.fighter import Fighter as es_Fighter
from eos.saveddata.implant import Implant as es_Implant
from eos.saveddata.ship import Ship as es_Ship
from eos.saveddata.module import Module as es_Module, State, Slot
from eos.saveddata.fit import Fit as FitType
from service.character import Character
from service.damagePattern import DamagePattern
from service.settings import SettingsProvider

pyfalog = Logger(__name__)


class Fit(object):
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Fit()

        return cls.instance

    def __init__(self):
        pyfalog.debug("Initialize Fit class")
        self.pattern = DamagePattern.getInstance().getDamagePattern("Uniform")
        self.targetResists = None
        self.character = saveddata_Character.getAll5()
        self.booster = False
        self.dirtyFitIDs = set()

        serviceFittingDefaultOptions = {
            "useGlobalCharacter": False,
            "useGlobalDamagePattern": False,
            "defaultCharacter": self.character.ID,
            "useGlobalForceReload": False,
            "colorFitBySlot": False,
            "rackSlots": True,
            "rackLabels": True,
            "compactSkills": True,
            "showTooltip": True,
            "showMarketShortcuts": False,
            "enableGaugeAnimation": True,
            "exportCharges": True,
            "openFitInNew": False,
            "priceSystem": "Jita",
            "priceSource": "eve-marketdata.com",
            "showShipBrowserTooltip": True,
            "marketSearchDelay": 250
        }

        self.serviceFittingOptions = SettingsProvider.getInstance().getSettings(
            "pyfaServiceFittingOptions", serviceFittingDefaultOptions)

    @staticmethod
    def getAllFits():
        pyfalog.debug("Fetching all fits")
        fits = eos.db.getFitList()
        return fits

    @staticmethod
    def getFitsWithShip(shipID):
        """ Lists fits of shipID, used with shipBrowser """
        pyfalog.debug("Fetching all fits for ship ID: {0}", shipID)
        fits = eos.db.getFitsWithShip(shipID)
        names = []
        for fit in fits:
            names.append((fit.ID, fit.name, fit.booster, fit.modified or fit.created or datetime.datetime.fromtimestamp(fit.timestamp), fit.notes, fit.ship.item.graphicID))

        return names

    @staticmethod
    def getRecentFits():
        """ Fetches recently modified fits, used with shipBrowser """
        pyfalog.debug("Fetching recent fits")
        fits = eos.db.getRecentFits()
        returnInfo = []

        for fit in fits:
            item = eos.db.getItem(fit[1])
            returnInfo.append((fit[0], fit[2], fit[3] or fit[4] or datetime.datetime.fromtimestamp(fit[5]), item, fit[6]))
            #                  ID      name    timestamps                                                   item  notes

        return returnInfo

    @staticmethod
    def getFitsWithModules(typeIDs):
        """ Lists fits flagged as booster """
        fits = eos.db.getFitsWithModules(typeIDs)
        return fits

    @staticmethod
    def countAllFits():
        pyfalog.debug("Getting count of all fits.")
        return eos.db.countAllFits()

    @staticmethod
    def countFitsWithShip(stuff):
        pyfalog.debug("Getting count of all fits for: {0}", stuff)
        count = eos.db.countFitsWithShip(stuff)
        return count

    @staticmethod
    def getModule(fitID, pos):
        fit = eos.db.getFit(fitID)
        return fit.modules[pos]

    def newFit(self, shipID, name=None):
        pyfalog.debug("Creating new fit for ID: {0}", shipID)
        try:
            ship = es_Ship(eos.db.getItem(shipID))
        except ValueError:
            ship = es_Citadel(eos.db.getItem(shipID))
        fit = FitType(ship)
        fit.name = name if name is not None else "New %s" % fit.ship.item.name
        fit.damagePattern = self.pattern
        fit.targetResists = self.targetResists
        fit.character = self.character
        fit.booster = self.booster
        eos.db.save(fit)
        self.recalc(fit)
        return fit.ID

    @staticmethod
    def toggleBoostFit(fitID):
        pyfalog.debug("Toggling as booster for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        fit.booster = not fit.booster
        eos.db.commit()

    @staticmethod
    def renameFit(fitID, newName):
        pyfalog.debug("Renaming fit ({0}) to: {1}", fitID, newName)
        fit = eos.db.getFit(fitID)
        fit.name = newName
        eos.db.commit()

    @staticmethod
    def deleteFit(fitID):
        fit = eos.db.getFit(fitID)
        pyfalog.debug("Fit::deleteFit - Deleting fit: {}", fit)

        # refresh any fits this fit is projected onto. Otherwise, if we have
        # already loaded those fits, they will not reflect the changes

        # A note on refreshFits: we collect the target fits in a set because
        # if a target fit has the same fit for both projected and command,
        # it will be refreshed first during the projected loop and throw an
        # error during the command loop
        refreshFits = set()
        for projection in list(fit.projectedOnto.values()):
            if projection.victim_fit != fit and projection.victim_fit in eos.db.saveddata_session:  # GH issue #359
                refreshFits.add(projection.victim_fit)

        for booster in list(fit.boostedOnto.values()):
            if booster.boosted_fit != fit and booster.boosted_fit in eos.db.saveddata_session:  # GH issue #359
                refreshFits.add(booster.boosted_fit)

        eos.db.remove(fit)

        pyfalog.debug("    Need to refresh {} fits: {}", len(refreshFits), refreshFits)
        for fit in refreshFits:
            eos.db.saveddata_session.refresh(fit)

        eos.db.saveddata_session.commit()

    @staticmethod
    def copyFit(fitID):
        pyfalog.debug("Creating copy of fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        newFit = copy.deepcopy(fit)
        eos.db.save(newFit)
        return newFit.ID

    @staticmethod
    def clearFit(fitID):
        pyfalog.debug("Clearing fit for fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        fit.clear()
        return fit

    @staticmethod
    def editNotes(fitID, notes):
        fit = eos.db.getFit(fitID)
        if fit:
            fit.notes = notes
            eos.db.commit()

    def toggleFactorReload(self, fitID):
        pyfalog.debug("Toggling factor reload for fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        fit.factorReload = not fit.factorReload
        eos.db.commit()
        self.recalc(fit)

    def switchFit(self, fitID):
        pyfalog.debug("Switching fit to fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)

        if self.serviceFittingOptions["useGlobalCharacter"]:
            if fit.character != self.character:
                fit.calculated = False
                fit.character = self.character

        if self.serviceFittingOptions["useGlobalDamagePattern"]:
            if fit.damagePattern != self.pattern:
                fit.calculated = False
                fit.damagePattern = self.pattern

        eos.db.commit()

        if not fit.calculated:
            self.recalc(fit)

    def getFit(self, fitID, projected=False, basic=False):
        """
        Gets fit from database

        Projected is a recursion flag that is set to reduce recursions into projected fits
        Basic is a flag to simply return the fit without any other processing
        """
        # pyfalog.debug("Getting fit for fit ID: {0}", fitID)
        if fitID is None:
            return None
        fit = eos.db.getFit(fitID)

        if fit is None:
            return None

        if basic:
            return fit

        inited = getattr(fit, "inited", None)

        if inited is None or inited is False:
            if not projected:
                for fitP in fit.projectedFits:
                    self.getFit(fitP.ID, projected=True)
                self.recalc(fit)
                fit.fill()

                # this will loop through modules and set their restriction flag (set in m.fit())
                if fit.ignoreRestrictions:
                    for mod in fit.modules:
                        if not mod.isEmpty:
                            mod.fits(fit)

            # Check that the states of all modules are valid
            self.checkStates(fit, None)

            eos.db.commit()
            fit.inited = True
        return fit

    @staticmethod
    def searchFits(name):
        pyfalog.debug("Searching for fit: {0}", name)
        results = eos.db.searchFits(name)
        fits = []

        for fit in sorted(results, key=lambda f: (f.ship.item.group.name, f.ship.item.name, f.name)):
            fits.append((
                fit.ID,
                fit.name,
                fit.ship.item.ID,
                fit.ship.item.name,
                fit.booster,
                fit.modifiedCoalesce,
                fit.notes))
        return fits

    def addImplant(self, fitID, itemID, recalc=True):
        pyfalog.debug("Adding implant to fit ({0}) for item ID: {1}", fitID, itemID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager="attributes")
        try:
            implant = es_Implant(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", itemID)
            return False

        fit.implants.append(implant)
        if recalc:
            self.recalc(fit)
        return True

    def removeImplant(self, fitID, position, recalc=True):
        pyfalog.debug("Removing implant from position ({0}) for fit ID: {1}", position, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        implant = fit.implants[position]
        fit.implants.remove(implant)
        if recalc:
            self.recalc(fit)
        return True

    def addBooster(self, fitID, itemID, recalc=True):
        pyfalog.debug("Adding booster ({0}) to fit ID: {1}", itemID, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager="attributes")
        try:
            booster = es_Booster(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", itemID)
            return False

        fit.boosters.append(booster)
        if recalc:
            self.recalc(fit)
        return True

    def removeBooster(self, fitID, position, recalc=True):
        pyfalog.debug("Removing booster from position ({0}) for fit ID: {1}", position, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        booster = fit.boosters[position]
        fit.boosters.remove(booster)
        if recalc:
            self.recalc(fit)
        return True

    def project(self, fitID, thing):
        pyfalog.debug("Projecting fit ({0}) onto: {1}", fitID, thing)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)

        if isinstance(thing, int):
            thing = eos.db.getItem(thing,
                                   eager=("attributes", "group.category"))

        if isinstance(thing, es_Module):
            thing = copy.deepcopy(thing)
            fit.projectedModules.append(thing)
        elif isinstance(thing, FitType):
            if thing in fit.projectedFits:
                return

            fit.__projectedFits[thing.ID] = thing

            # this bit is required -- see GH issue # 83
            eos.db.saveddata_session.flush()
            eos.db.saveddata_session.refresh(thing)
        elif thing.category.name == "Drone":
            drone = None
            for d in fit.projectedDrones.find(thing):
                if d is None or d.amountActive == d.amount or d.amount >= 5:
                    drone = d
                    break

            if drone is None:
                drone = es_Drone(thing)
                fit.projectedDrones.append(drone)

            drone.amount += 1
        elif thing.category.name == "Fighter":
            fighter = es_Fighter(thing)
            fit.projectedFighters.append(fighter)
        elif thing.group.name in es_Module.SYSTEM_GROUPS:
            module = es_Module(thing)
            module.state = State.ONLINE
            fit.projectedModules.append(module)
        else:
            try:
                module = es_Module(thing)
            except ValueError:
                return False
            module.state = State.ACTIVE
            if not module.canHaveState(module.state, fit):
                module.state = State.OFFLINE
            fit.projectedModules.append(module)

        eos.db.commit()
        self.recalc(fit)
        return True

    def addCommandFit(self, fitID, thing):
        pyfalog.debug("Projecting command fit ({0}) onto: {1}", fitID, thing)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)

        if thing in fit.commandFits:
            return

        fit.__commandFits[thing.ID] = thing

        # this bit is required -- see GH issue # 83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(thing)

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleProjected(self, fitID, thing, click):
        pyfalog.debug("Toggling projected on fit ({0}) for: {1}", fitID, thing)
        fit = eos.db.getFit(fitID)
        if isinstance(thing, es_Drone):
            if thing.amountActive == 0 and thing.canBeApplied(fit):
                thing.amountActive = thing.amount
            else:
                thing.amountActive = 0
        elif isinstance(thing, es_Fighter):
            thing.active = not thing.active
        elif isinstance(thing, es_Module):
            thing.state = self.__getProposedState(thing, click)
            if not thing.canHaveState(thing.state, fit):
                thing.state = State.OFFLINE
        elif isinstance(thing, FitType):
            projectionInfo = thing.getProjectionInfo(fitID)
            if projectionInfo:
                projectionInfo.active = not projectionInfo.active

        eos.db.commit()
        self.recalc(fit)

    def toggleCommandFit(self, fitID, thing):
        pyfalog.debug("Toggle command fit ({0}) for: {1}", fitID, thing)
        fit = eos.db.getFit(fitID)
        commandInfo = thing.getCommandInfo(fitID)
        if commandInfo:
            commandInfo.active = not commandInfo.active

        eos.db.commit()
        self.recalc(fit)

    def changeAmount(self, fitID, projected_fit, amount):
        """Change amount of projected fits"""
        pyfalog.debug("Changing fit ({0}) for projected fit ({1}) to new amount: {2}", fitID, projected_fit.getProjectionInfo(fitID), amount)
        fit = eos.db.getFit(fitID)
        amount = min(20, max(1, amount))  # 1 <= a <= 20
        projectionInfo = projected_fit.getProjectionInfo(fitID)
        if projectionInfo:
            projectionInfo.amount = amount

        eos.db.commit()
        self.recalc(fit)

    def changeActiveFighters(self, fitID, fighter, amount):
        pyfalog.debug("Changing active fighters ({0}) for fit ({1}) to amount: {2}", fighter.itemID, fitID, amount)
        fit = eos.db.getFit(fitID)
        fighter.amountActive = amount

        eos.db.commit()
        self.recalc(fit)

    def removeProjected(self, fitID, thing):
        pyfalog.debug("Removing projection on fit ({0}) from: {1}", fitID, thing)
        fit = eos.db.getFit(fitID)
        if isinstance(thing, es_Drone):
            fit.projectedDrones.remove(thing)
        elif isinstance(thing, es_Module):
            fit.projectedModules.remove(thing)
        elif isinstance(thing, es_Fighter):
            fit.projectedFighters.remove(thing)
        else:
            del fit.__projectedFits[thing.ID]
            # fit.projectedFits.remove(thing)

        eos.db.commit()
        self.recalc(fit)

    def removeCommand(self, fitID, thing):
        pyfalog.debug("Removing command projection from fit ({0}) for: {1}", fitID, thing)
        fit = eos.db.getFit(fitID)
        del fit.__commandFits[thing.ID]

        eos.db.commit()
        self.recalc(fit)

    def changeMutatedValue(self, mutator, value):
        pyfalog.debug("Changing mutated value for {} / {}: {} => {}".format(mutator.module, mutator.module.mutaplasmid, mutator.value, value))
        mutator.value = value

        eos.db.commit()
        return mutator.value

    def appendModule(self, fitID, itemID):
        pyfalog.debug("Appending module for fit ({0}) using item: {1}", fitID, itemID)
        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        try:
            m = es_Module(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", itemID)
            return False

        if m.item.category.name == "Subsystem":
            fit.modules.freeSlot(m.getModifiedItemAttr("subSystemSlot"))

        if m.fits(fit):
            m.owner = fit
            numSlots = len(fit.modules)
            fit.modules.append(m)
            if m.isValidState(State.ACTIVE):
                m.state = State.ACTIVE

            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            self.checkStates(fit, m)

            fit.fill()
            eos.db.commit()

            return numSlots != len(fit.modules)
        else:
            return None

    def removeModule(self, fitID, positions):
        """Removes modules based on a number of positions."""
        pyfalog.debug("Removing module from position ({0}) for fit ID: {1}", positions, fitID)
        fit = eos.db.getFit(fitID)

        # Convert scalar value to list
        if not isinstance(positions, list):
            positions = [positions]

        modulesChanged = False
        for x in positions:
            if not fit.modules[x].isEmpty:
                fit.modules.toDummy(x)
                modulesChanged = True

        # if no modules have changes, report back None
        if not modulesChanged:
            return None

        numSlots = len(fit.modules)
        self.recalc(fit)
        self.checkStates(fit, None)
        fit.fill()
        eos.db.commit()
        return numSlots != len(fit.modules)

    def convertMutaplasmid(self, fitID, position, mutaplasmid):
        # this is mostly the same thing as the self.changeModule method, however it initializes an abyssal module with
        # the old module as it's base, and then replaces it
        fit = eos.db.getFit(fitID)
        base = fit.modules[position]
        fit.modules.toDummy(position)

        try:
            m = es_Module(mutaplasmid.resultingItem, base.item, mutaplasmid)
        except ValueError:
            pyfalog.warning("Invalid item: {0} AHHHH")
            return False

        if m.fits(fit):
            m.owner = fit
            fit.modules.toModule(position, m)
            if m.isValidState(State.ACTIVE):
                m.state = State.ACTIVE

            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            self.checkStates(fit, m)

            fit.fill()
            eos.db.commit()

            return True
        else:
            return None

    def changeModule(self, fitID, position, newItemID):
        fit = eos.db.getFit(fitID)

        # We're trying to add a charge to a slot, which won't work. Instead, try to add the charge to the module in that slot.
        if self.isAmmo(newItemID):
            module = fit.modules[position]
            if not module.isEmpty:
                self.setAmmo(fitID, newItemID, [module])
            return True

        pyfalog.debug("Changing position of module from position ({0}) for fit ID: {1}", position, fitID)

        item = eos.db.getItem(newItemID, eager=("attributes", "group.category"))

        # Dummy it out in case the next bit fails
        fit.modules.toDummy(position)

        try:
            m = es_Module(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", newItemID)
            return False

        if m.fits(fit):
            m.owner = fit
            fit.modules.toModule(position, m)
            if m.isValidState(State.ACTIVE):
                m.state = State.ACTIVE

            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            self.checkStates(fit, m)

            fit.fill()
            eos.db.commit()

            return True
        else:
            return None

    def moveCargoToModule(self, fitID, moduleIdx, cargoIdx, copyMod=False):
        """
        Moves cargo to fitting window. Can either do a copy, move, or swap with current module
        If we try to copy/move into a spot with a non-empty module, we swap instead.
        To avoid redundancy in converting Cargo item, this function does the
        sanity checks as opposed to the GUI View. This is different than how the
        normal .swapModules() does things, which is mostly a blind swap.
        """

        fit = eos.db.getFit(fitID)
        module = fit.modules[moduleIdx]
        cargo = fit.cargo[cargoIdx]

        # We're trying to move a charge from cargo to a slot - try to add charge to dst module. Don't do anything with
        # the charge in the cargo (don't respect move vs copy)
        if self.isAmmo(cargo.item.ID):
            if not module.isEmpty:
                self.setAmmo(fitID, cargo.item.ID, [module])
            return

        pyfalog.debug("Moving cargo item to module for fit ID: {0}", fitID)

        # Gather modules and convert Cargo item to Module, silently return if not a module
        try:
            cargoP = es_Module(cargo.item)
            cargoP.owner = fit
            if cargoP.isValidState(State.ACTIVE):
                cargoP.state = State.ACTIVE
        except:
            pyfalog.warning("Invalid item: {0}", cargo.item)
            return

        if cargoP.slot != module.slot:  # can't swap modules to different racks
            return

        # remove module that we are trying to move cargo to
        fit.modules.remove(module)

        if not cargoP.fits(fit):  # if cargo doesn't fit, rollback and return
            fit.modules.insert(moduleIdx, module)
            return

        fit.modules.insert(moduleIdx, cargoP)

        if not copyMod:  # remove existing cargo if not cloning
            if cargo.amount == 1:
                fit.cargo.remove(cargo)
            else:
                cargo.amount -= 1

        if not module.isEmpty:  # if module is placeholder, we don't want to convert/add it
            moduleItem = module.item if not module.item.isAbyssal else module.baseItem
            for x in fit.cargo.find(moduleItem ):
                x.amount += 1
                break
            else:
                moduleP = es_Cargo(moduleItem )
                moduleP.amount = 1
                fit.cargo.insert(cargoIdx, moduleP)

        eos.db.commit()
        self.recalc(fit)

    @staticmethod
    def swapModules(fitID, src, dst):
        pyfalog.debug("Swapping modules from source ({0}) to destination ({1}) for fit ID: {1}", src, dst, fitID)
        fit = eos.db.getFit(fitID)
        # Gather modules
        srcMod = fit.modules[src]
        dstMod = fit.modules[dst]

        # To swap, we simply remove mod and insert at destination.
        fit.modules.remove(srcMod)
        fit.modules.insert(dst, srcMod)
        fit.modules.remove(dstMod)
        fit.modules.insert(src, dstMod)

        eos.db.commit()

    def cloneModule(self, fitID, src, dst):
        """
        Clone a module from src to dst
        This will overwrite dst! Checking for empty module must be
        done at a higher level
        """
        pyfalog.debug("Cloning modules from source ({0}) to destination ({1}) for fit ID: {1}", src, dst, fitID)
        fit = eos.db.getFit(fitID)
        # Gather modules
        srcMod = fit.modules[src]
        dstMod = fit.modules[dst]  # should be a placeholder module

        new = copy.deepcopy(srcMod)
        new.owner = fit
        if new.fits(fit):
            # insert copy if module meets hardpoint restrictions
            fit.modules.remove(dstMod)
            fit.modules.insert(dst, new)

            eos.db.commit()
            self.recalc(fit)

    def addCargo(self, fitID, itemID, amount=1, replace=False):
        """
        Adds cargo via typeID of item. If replace = True, we replace amount with
        given parameter, otherwise we increment
        """
        pyfalog.debug("Adding cargo ({0}) fit ID: {1}", itemID, fitID)

        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID)
        cargo = None

        # adding from market
        for x in fit.cargo.find(item):
            if x is not None:
                # found item already in cargo, use previous value and remove old
                cargo = x
                fit.cargo.remove(x)
                break

        if cargo is None:
            # if we don't have the item already in cargo, use default values
            cargo = es_Cargo(item)

        fit.cargo.append(cargo)
        if replace:
            cargo.amount = amount
        else:
            cargo.amount += amount

        self.recalc(fit)
        eos.db.commit()

        return True

    def removeCargo(self, fitID, position):
        pyfalog.debug("Removing cargo from position ({0}) fit ID: {1}", position, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        charge = fit.cargo[position]
        fit.cargo.remove(charge)
        self.recalc(fit)
        return True

    def addFighter(self, fitID, itemID, recalc=True):
        pyfalog.debug("Adding fighters ({0}) to fit ID: {1}", itemID, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        if item.category.name == "Fighter":
            fighter = None
            '''
            for d in fit.fighters.find(item):
                if d is not None and d.amountActive == 0 and d.amount < max(5, fit.extraAttributes["maxActiveDrones"]):
                    drone = d
                    break
            '''
            if fighter is None:
                fighter = es_Fighter(item)
                used = fit.getSlotsUsed(fighter.slot)
                total = fit.getNumSlots(fighter.slot)
                standardAttackActive = False
                for ability in fighter.abilities:
                    if ability.effect.isImplemented and ability.effect.handlerName == 'fighterabilityattackm':
                        # Activate "standard attack" if available
                        ability.active = True
                        standardAttackActive = True
                    else:
                        # Activate all other abilities (Neut, Web, etc) except propmods if no standard attack is active
                        if ability.effect.isImplemented and \
                                standardAttackActive is False and \
                                ability.effect.handlerName != 'fighterabilitymicrowarpdrive' and \
                                ability.effect.handlerName != 'fighterabilityevasivemaneuvers':
                            ability.active = True

                if used >= total:
                    fighter.active = False

                if fighter.fits(fit) is True:
                    fit.fighters.append(fighter)
                else:
                    return False

            eos.db.commit()
            if recalc:
                self.recalc(fit)
            return True
        else:
            return False

    def removeFighter(self, fitID, i, recalc=True):
        pyfalog.debug("Removing fighters from fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        f = fit.fighters[i]
        fit.fighters.remove(f)

        eos.db.commit()
        if recalc:
            self.recalc(fit)
        return True

    def addDrone(self, fitID, itemID, numDronesToAdd=1, recalc=True):
        pyfalog.debug("Adding {0} drones ({1}) to fit ID: {2}", numDronesToAdd, itemID, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        if item.category.name == "Drone":
            drone = None
            for d in fit.drones.find(item):
                if d is not None and d.amountActive == 0 and d.amount < max(5, fit.extraAttributes["maxActiveDrones"]):
                    drone = d
                    break

            if drone is None:
                drone = es_Drone(item)
                if drone.fits(fit) is True:
                    fit.drones.append(drone)
                else:
                    return False
            drone.amount += numDronesToAdd
            eos.db.commit()
            if recalc:
                self.recalc(fit)
            return True
        else:
            return False

    def mergeDrones(self, fitID, d1, d2, projected=False):
        pyfalog.debug("Merging drones on fit ID: {0}", fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        if d1.item != d2.item:
            return False

        if projected:
            fit.projectedDrones.remove(d1)
        else:
            fit.drones.remove(d1)

        d2.amount += d1.amount
        d2.amountActive += d1.amountActive

        # If we have less than the total number of drones active, make them all active. Fixes #728
        # This could be removed if we ever add an enhancement to make drone stacks partially active.
        if d2.amount > d2.amountActive:
            d2.amountActive = d2.amount

        eos.db.commit()
        self.recalc(fit)
        return True

    @staticmethod
    def splitDrones(fit, d, amount, l):
        pyfalog.debug("Splitting drones for fit ID: {0}", fit)
        total = d.amount
        active = d.amountActive > 0
        d.amount = amount
        d.amountActive = amount if active else 0

        newD = es_Drone(d.item)
        newD.amount = total - amount
        newD.amountActive = newD.amount if active else 0
        l.append(newD)
        eos.db.commit()

    def splitProjectedDroneStack(self, fitID, d, amount):
        pyfalog.debug("Splitting projected drone stack for fit ID: {0}", fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        self.splitDrones(fit, d, amount, fit.projectedDrones)

    def splitDroneStack(self, fitID, d, amount):
        pyfalog.debug("Splitting drone stack for fit ID: {0}", fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        self.splitDrones(fit, d, amount, fit.drones)

    def removeDrone(self, fitID, i, numDronesToRemove=1, recalc=True):
        pyfalog.debug("Removing {0} drones for fit ID: {1}", numDronesToRemove, fitID)
        fit = eos.db.getFit(fitID)
        d = fit.drones[i]
        d.amount -= numDronesToRemove
        if d.amountActive > 0:
            d.amountActive -= numDronesToRemove

        if d.amount == 0:
            del fit.drones[i]

        eos.db.commit()
        if recalc:
            self.recalc(fit)
        return True

    def toggleDrone(self, fitID, i):
        pyfalog.debug("Toggling drones for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        d = fit.drones[i]
        if d.amount == d.amountActive:
            d.amountActive = 0
        else:
            d.amountActive = d.amount

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleFighter(self, fitID, i):
        pyfalog.debug("Toggling fighters for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        f = fit.fighters[i]
        f.active = not f.active

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleImplant(self, fitID, i):
        pyfalog.debug("Toggling implant for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        implant = fit.implants[i]
        implant.active = not implant.active

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleImplantSource(self, fitID, source):
        pyfalog.debug("Toggling implant source for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        fit.implantSource = source

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleRestrictionIgnore(self, fitID):
        pyfalog.debug("Toggling restriction ignore for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        fit.ignoreRestrictions = not fit.ignoreRestrictions

        # remove invalid modules when switching back to enabled fitting restrictions
        if not fit.ignoreRestrictions:
            for m in fit.modules:
                if not m.isEmpty and not m.fits(fit, False):
                    self.removeModule(fit.ID, m.modPosition)

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleBooster(self, fitID, i):
        pyfalog.debug("Toggling booster for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        booster = fit.boosters[i]
        booster.active = not booster.active

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleFighterAbility(self, fitID, ability):
        pyfalog.debug("Toggling fighter ability for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        ability.active = not ability.active
        eos.db.commit()
        self.recalc(fit)

    def toggleBoosterSideEffect(self, fitID, sideEffect):
        pyfalog.debug("Toggling booster side effect for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        sideEffect.active = not sideEffect.active
        eos.db.commit()
        self.recalc(fit)

    def changeChar(self, fitID, charID):
        pyfalog.debug("Changing character ({0}) for fit ID: {1}", charID, fitID)
        if fitID is None or charID is None:
            if charID is not None:
                self.character = Character.getInstance().all5()

            return

        fit = eos.db.getFit(fitID)
        fit.character = self.character = eos.db.getCharacter(charID)
        self.recalc(fit)

    @staticmethod
    def isAmmo(itemID):
        return eos.db.getItem(itemID).category.name == "Charge"

    def setAmmo(self, fitID, ammoID, modules):
        pyfalog.debug("Set ammo for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        ammo = eos.db.getItem(ammoID) if ammoID else None

        for mod in modules:
            if mod.isValidCharge(ammo):
                mod.charge = ammo

        self.recalc(fit)

    @staticmethod
    def getTargetResists(fitID):
        pyfalog.debug("Get target resists for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        return fit.targetResists

    def setTargetResists(self, fitID, pattern):
        pyfalog.debug("Set target resist for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.targetResists = pattern
        eos.db.commit()

        self.recalc(fit)

    @staticmethod
    def getDamagePattern(fitID):
        pyfalog.debug("Get damage pattern for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        return fit.damagePattern

    def setDamagePattern(self, fitID, pattern):
        pyfalog.debug("Set damage pattern for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.damagePattern = self.pattern = pattern
        eos.db.commit()

        self.recalc(fit)

    def setMode(self, fitID, mode):
        pyfalog.debug("Set mode for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.mode = mode
        eos.db.commit()

        self.recalc(fit)

    def setAsPattern(self, fitID, ammo):
        pyfalog.debug("Set as pattern for fit ID: {0}", fitID)
        if fitID is None:
            return

        sDP = DamagePattern.getInstance()
        dp = sDP.getDamagePattern("Selected Ammo")
        if dp is None:
            dp = es_DamagePattern()
            dp.name = "Selected Ammo"

        fit = eos.db.getFit(fitID)
        for attr in ("em", "thermal", "kinetic", "explosive"):
            setattr(dp, "%sAmount" % attr, ammo.getAttribute("%sDamage" % attr) or 0)

        fit.damagePattern = dp
        self.recalc(fit)

    def checkStates(self, fit, base):
        pyfalog.debug("Check states for fit ID: {0}", fit)
        changed = False
        for mod in fit.modules:
            if mod != base:
                # fix for #529, where a module may be in incorrect state after CCP changes mechanics of module
                if not mod.canHaveState(mod.state) or not mod.isValidState(mod.state):
                    mod.state = State.ONLINE
                    changed = True

        for mod in fit.projectedModules:
            # fix for #529, where a module may be in incorrect state after CCP changes mechanics of module
            if not mod.canHaveState(mod.state, fit) or not mod.isValidState(mod.state):
                mod.state = State.OFFLINE
                changed = True

        for drone in fit.projectedDrones:
            if drone.amountActive > 0 and not drone.canBeApplied(fit):
                drone.amountActive = 0
                changed = True

        # If any state was changed, recalculate attributes again
        if changed:
            self.recalc(fit)

    def toggleModulesState(self, fitID, base, modules, click):
        pyfalog.debug("Toggle module state for fit ID: {0}", fitID)
        changed = False
        proposedState = self.__getProposedState(base, click)

        if proposedState != base.state:
            changed = True
            base.state = proposedState
            for mod in modules:
                if mod != base:
                    p = self.__getProposedState(mod, click, proposedState)
                    mod.state = p
                    if p != mod.state:
                        changed = True

        if changed:
            eos.db.commit()
            fit = eos.db.getFit(fitID)

            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            self.checkStates(fit, base)

    # Old state : New State
    localMap = {
        State.OVERHEATED: State.ACTIVE,
        State.ACTIVE: State.ONLINE,
        State.OFFLINE: State.ONLINE,
        State.ONLINE: State.ACTIVE}
    projectedMap = {
        State.OVERHEATED: State.ACTIVE,
        State.ACTIVE: State.OFFLINE,
        State.OFFLINE: State.ACTIVE,
        State.ONLINE: State.ACTIVE}  # Just in case
    # For system effects. They should only ever be online or offline
    projectedSystem = {
        State.OFFLINE: State.ONLINE,
        State.ONLINE: State.OFFLINE}

    def __getProposedState(self, mod, click, proposedState=None):
        pyfalog.debug("Get proposed state for module.")
        if mod.slot == Slot.SUBSYSTEM or mod.isEmpty:
            return State.ONLINE

        if mod.slot == Slot.SYSTEM:
            transitionMap = self.projectedSystem
        else:
            transitionMap = self.projectedMap if mod.projected else self.localMap

        currState = mod.state

        if proposedState is not None:
            state = proposedState
        elif click == "right":
            state = State.OVERHEATED
        elif click == "ctrl":
            state = State.OFFLINE
        else:
            state = transitionMap[currState]
            if not mod.isValidState(state):
                state = -1

        if mod.isValidState(state):
            return state
        else:
            return currState

    def refreshFit(self, fitID):
        pyfalog.debug("Refresh fit for fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        eos.db.commit()
        self.recalc(fit)

    def recalc(self, fit):
        start_time = time()
        pyfalog.info("=" * 10 + "recalc: {0}" + "=" * 10, fit.name)

        fit.factorReload = self.serviceFittingOptions["useGlobalForceReload"]
        fit.clear()

        fit.calculateModifiedAttributes()

        pyfalog.info("=" * 10 + "recalc time: " + str(time() - start_time) + "=" * 10)
