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

import eos.db
from eos.saveddata.booster import Booster as es_Booster
from eos.saveddata.cargo import Cargo as es_Cargo

from eos.saveddata.drone import Drone as es_Drone
from eos.saveddata.fighter import Fighter as es_Fighter
from eos.saveddata.implant import Implant as es_Implant
from eos.saveddata.module import Module as es_Module, State
from eos.saveddata.fit import Fit as FitType
from utils.deprecated import deprecated

pyfalog = Logger(__name__)


class FitDeprecated(object):

    @staticmethod
    @deprecated
    def renameFit(fitID, newName):
        pyfalog.debug("Renaming fit ({0}) to: {1}", fitID, newName)
        fit = eos.db.getFit(fitID)
        old_name = fit.name
        fit.name = newName
        eos.db.commit()
        return old_name, newName

    @deprecated
    def toggleImplantSource(self, fitID, source):
        pyfalog.debug("Toggling implant source for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        fit.implantSource = source

        eos.db.commit()
        self.recalc(fit)
        return True

    @deprecated
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

    @deprecated
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
    @deprecated
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

    @deprecated
    def splitProjectedDroneStack(self, fitID, d, amount):
        pyfalog.debug("Splitting projected drone stack for fit ID: {0}", fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        self.splitDrones(fit, d, amount, fit.projectedDrones)

    @deprecated
    def splitDroneStack(self, fitID, d, amount):
        pyfalog.debug("Splitting drone stack for fit ID: {0}", fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        self.splitDrones(fit, d, amount, fit.drones)

    @deprecated
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

    @deprecated
    def changeAmount(self, fitID, projected_fit, amount):
        """Change amount of projected fits"""
        pyfalog.debug("Changing fit ({0}) for projected fit ({1}) to new amount: {2}", fitID,
                      projected_fit.getProjectionInfo(fitID), amount)
        fit = eos.db.getFit(fitID)
        amount = min(20, max(1, amount))  # 1 <= a <= 20
        projectionInfo = projected_fit.getProjectionInfo(fitID)
        if projectionInfo:
            projectionInfo.amount = amount

        eos.db.commit()
        self.recalc(fit)

    @deprecated
    def changeActiveFighters(self, fitID, fighter, amount):
        pyfalog.debug("Changing active fighters ({0}) for fit ({1}) to amount: {2}", fighter.itemID, fitID, amount)
        fit = eos.db.getFit(fitID)
        fighter.amountActive = amount

        eos.db.commit()
        self.recalc(fit)

    @deprecated
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

    @deprecated
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

    @deprecated
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

    @deprecated
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

    @deprecated
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

    @deprecated
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

            fit.projectedFitDict[thing.ID] = thing

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

    @deprecated
    def addCommandFit(self, fitID, thing):
        pyfalog.debug("Projecting command fit ({0}) onto: {1}", fitID, thing)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)

        if thing in fit.commandFits:
            return

        fit.commandFitDict[thing.ID] = thing

        # this bit is required -- see GH issue # 83
        eos.db.saveddata_session.flush()
        eos.db.saveddata_session.refresh(thing)

        eos.db.commit()
        self.recalc(fit)
        return True

    @deprecated
    def toggleCommandFit(self, fitID, thing):
        pyfalog.debug("Toggle command fit ({0}) for: {1}", fitID, thing)
        fit = eos.db.getFit(fitID)
        commandInfo = thing.getCommandInfo(fitID)
        if commandInfo:
            commandInfo.active = not commandInfo.active

        eos.db.commit()
        self.recalc(fit)

    @deprecated
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
            del fit.projectedFitDict[thing.ID]
            # fit.projectedFits.remove(thing)

        eos.db.commit()
        self.recalc(fit)

    @deprecated
    def removeCommand(self, fitID, thing):
        pyfalog.debug("Removing command projection from fit ({0}) for: {1}", fitID, thing)
        fit = eos.db.getFit(fitID)
        del fit.commandFitDict[thing.ID]

        eos.db.commit()
        self.recalc(fit)

    @deprecated
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

            return numSlots != len(fit.modules), m.modPosition
        else:
            return None, None

    @deprecated
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

    @deprecated
    def changeModule(self, fitID, position, newItemID, recalc=True):
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

            if recalc:
                # As some items may affect state-limiting attributes of the ship, calculate new attributes first
                self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            self.checkStates(fit, m)

            fit.fill()
            eos.db.commit()

            return m
        else:
            return None

    @deprecated
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
            for x in fit.cargo.find(moduleItem):
                x.amount += 1
                break
            else:
                moduleP = es_Cargo(moduleItem)
                moduleP.amount = 1
                fit.cargo.insert(cargoIdx, moduleP)

        eos.db.commit()
        self.recalc(fit)

    @staticmethod
    @deprecated
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

    @deprecated
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

    @deprecated
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

    @deprecated
    def removeCargo(self, fitID, position):
        pyfalog.debug("Removing cargo from position ({0}) fit ID: {1}", position, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        charge = fit.cargo[position]
        fit.cargo.remove(charge)
        self.recalc(fit)
        return True

    @deprecated
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

    @deprecated
    def removeFighter(self, fitID, i, recalc=True):
        pyfalog.debug("Removing fighters from fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        f = fit.fighters[i]
        fit.fighters.remove(f)

        eos.db.commit()
        if recalc:
            self.recalc(fit)
        return True

    @deprecated
    def toggleFighter(self, fitID, i):
        pyfalog.debug("Toggling fighters for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        f = fit.fighters[i]
        f.active = not f.active

        eos.db.commit()
        self.recalc(fit)
        return True

    @deprecated
    def toggleImplant(self, fitID, i):
        pyfalog.debug("Toggling implant for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        implant = fit.implants[i]
        implant.active = not implant.active

        eos.db.commit()
        self.recalc(fit)
        return True

    @deprecated
    def toggleBooster(self, fitID, i):
        pyfalog.debug("Toggling booster for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        booster = fit.boosters[i]
        booster.active = not booster.active

        eos.db.commit()
        self.recalc(fit)
        return True

    @deprecated
    def setAmmo(self, fitID, ammoID, modules, recalc=True):
        pyfalog.debug("Set ammo for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        ammo = eos.db.getItem(ammoID) if ammoID else None

        for mod in modules:
            if mod.isValidCharge(ammo):
                mod.charge = ammo

        if recalc:
            self.recalc(fit)

    @deprecated
    def setMode(self, fitID, mode):
        pyfalog.debug("Set mode for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.mode = mode
        eos.db.commit()

        self.recalc(fit)

    @deprecated
    def toggleModulesState(self, fitID, base, modules, click):
        pyfalog.debug("Toggle module state for fit ID: {0}", fitID)
        changed = False
        proposedState = es_Module.getProposedState(base, click)

        if proposedState != base.state:
            changed = True
            base.state = proposedState
            for mod in modules:
                if mod != base:
                    p = es_Module.getProposedState(mod, click, proposedState)
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
