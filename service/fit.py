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

import eos.db
import eos.types
from eos.types import State, Slot
import copy
from service.damagePattern import DamagePattern

class Fit(object):
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Fit()

        return cls.instance


    def getFitsWithShip(self, id):
        fits = eos.db.getFitsWithShip(id)
        names = []
        for fit in fits:
            names.append((fit.ID, fit.name))

        return names

    def getModule(self, fitID, pos):
        fit = eos.db.getFit(fitID)
        return fit.modules[pos]

    def newFit(self, shipID, name):
        fit = eos.types.Fit()
        fit.ship = eos.types.Ship(eos.db.getItem(shipID))
        fit.name = name
        fit.damagePattern = DamagePattern.getInstance().getDamagePattern("Uniform")
        eos.db.save(fit)
        fit.calculateModifiedAttributes()
        return fit.ID

    def renameFit(self, fitID, newName):
        fit = eos.db.getFit(fitID)
        fit.name = newName
        eos.db.commit()

    def deleteFit(self, fitID):
        fit = eos.db.getFit(fitID)
        eos.db.remove(fit)

    def copyFit(self, fitID):
        fit = eos.db.getFit(fitID)
        newFit = copy.deepcopy(fit)
        eos.db.save(newFit)
        return newFit.ID

    def clearFit(self, fitID):
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        fit.clear()
        return fit

    def getFit(self, fitID):
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        fit.fill()
        eos.db.commit()
        fit.calculateModifiedAttributes()
        return fit

    def addImplant(self, fitID, itemID):
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        try:
            implant = eos.types.Implant(item)
        except ValueError:
            return False

        fit.implants.freeSlot(implant)
        fit.implants.append(implant)
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

    def removeImplant(self, fitID, position):
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        implant = fit.implants[position]
        fit.implants.remove(implant)
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

    def addBooster(self, fitID, itemID):
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        try:
            booster = eos.types.Booster(item)
        except ValueError:
            return False

        fit.boosters.freeSlot(booster)
        fit.boosters.append(booster)
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

    def removeBooster(self, fitID, position):
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        booster = fit.boosters[position]
        fit.boosters.remove(booster)
        fit.clear()
        fit.calculateModifiedAttributes()
        return True


    def appendModule(self, fitID, itemID):
        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        try:
            m = eos.types.Module(item)
        except ValueError:
            return False

        if m.fits(fit):
            numSlots = len(fit.modules)
            fit.modules.append(m)
            if m.isValidState(State.ACTIVE):
                m.state = State.ACTIVE

            fit.clear()
            fit.calculateModifiedAttributes()
            fit.fill()
            eos.db.commit()

            return numSlots != len(fit.modules)
        else:
            return None

    def removeModule(self, fitID, position):
        fit = eos.db.getFit(fitID)
        if fit.modules[position].isEmpty:
            return None

        numSlots = len(fit.modules)
        fit.modules.toDummy(position)
        fit.clear()
        fit.calculateModifiedAttributes()
        fit.fill()
        eos.db.commit()
        return numSlots != len(fit.modules)

    def swapModules(self, fitID, src, dst):
        fit = eos.db.getFit(fitID)
        m = fit.modules[src]
        fit.modules.remove(m)
        fit.modules.insert(dst, m)

    def addDrone(self, fitID, itemID):
        if fitID == None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        if item.category.name == "Drone":
            d = fit.drones.find(item)
            if d is None or d.amountActive == d.amount or d.amount >= 5:
                d = eos.types.Drone(item)
                fit.drones.append(d)

            d.amount += 1
            eos.db.commit()
            fit.clear()
            fit.calculateModifiedAttributes()
            return True
        else:
            return False

    def splitDroneStack(self, fitID, d, amount):
        if fitID == None:
            return False

        fit = eos.db.getFit(fitID)

        total = d.amount
        active = d.amountActive > 0
        d.amount = amount
        d.amountActive = amount if active else 0

        newD = eos.types.Drone(d.item)
        newD.amount = total - amount
        newD.amountActive = newD.amount if active else 0
        fit.drones.append(newD)
        eos.db.commit()

    def removeDrone(self, fitID, i):
        fit = eos.db.getFit(fitID)
        d = fit.drones[i]
        d.amount -= 1
        if d.amountActive > 0:
            d.amountActive -= 1

        if d.amount == 0:
            del fit.drones[i]

        eos.db.commit()
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

    def toggleDrone(self, fitID, i):
        fit = eos.db.getFit(fitID)
        d = fit.drones[i]
        if d.amount == d.amountActive:
            d.amountActive = 0
        else:
            d.amountActive = d.amount

        eos.db.commit()
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

    def toggleImplant(self, fitID, i):
        fit = eos.db.getFit(fitID)
        implant = fit.implants[i]
        implant.active = not implant.active

        eos.db.commit()
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

    def toggleBooster(self, fitID, i):
        fit = eos.db.getFit(fitID)
        booster = fit.boosters[i]
        booster.active = not booster.active

        eos.db.commit()
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

    def changeChar(self, fitID, charID):
        if fitID is None or charID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.character = eos.db.getCharacter(charID)
        fit.clear()
        fit.calculateModifiedAttributes()

    def isAmmo(self, itemID):
        return eos.db.getItem(itemID).category.name == "Charge"

    def setAmmo(self, fitID, ammoID, modules):
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        ammo = eos.db.getItem(ammoID)

        for pos in modules:
            mod = fit.modules[pos]
            if mod.isValidCharge(ammo):
                fit.modules[pos].charge = ammo

        fit.clear()
        fit.calculateModifiedAttributes()

    def setDamagePattern(self, fitID, pattern):
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.damagePattern = pattern
        eos.db.commit()
        fit.clear()
        fit.calculateModifiedAttributes()

    def exportFit(self, fitID):
        fit = eos.db.getFit(fitID)
        return fit.exportEft()

    def exportDna(self, fitID):
        fit = eos.db.getFit(fitID)
        return fit.exportDna()

    def exportXml(self, *fitIDs):
        fits = map(lambda id: eos.db.getFit(id), fitIDs)
        return eos.types.Fit.exportXml(*fits)

    def importFit(self, path):
        f = file(path)
        type, fits = eos.types.Fit.importAuto(f.read())

        return fits

    def importFitFromBuffer(self, buffer):
        type,fits = eos.types.Fit.importAuto(buffer)

        return fits

    def saveImportedFits(self, fits):
        for fit in fits:
            eos.db.save(fit)

    def toggleModulesState(self, fitID, base, modules, click):
        proposedState = self.__getProposedState(base, click)
        if proposedState != base.state:
            base.state = proposedState
            for mod in modules:
                if mod != base:
                    mod.state = self.__getProposedState(mod, click, proposedState)

        eos.db.commit()
        fit = eos.db.getFit(fitID)
        fit.clear()
        fit.calculateModifiedAttributes()

    # Old state : New State
    transitionMap = {State.OVERHEATED: State.ACTIVE,
                     State.ACTIVE: State.OFFLINE,
                     State.OFFLINE: State.ONLINE,
                     State.ONLINE: State.ACTIVE}

    def __getProposedState(self, mod, click, proposedState=None):
        if mod.slot in (Slot.RIG, Slot.SUBSYSTEM) or mod.isEmpty:
            return State.ONLINE

        currState = state = mod.state
        if proposedState is not None:
            state = proposedState
        elif click == "right":
            if currState == State.OVERHEATED:
                state = State.ACTIVE
            elif mod.isValidState(State.OVERHEATED):
                state = State.OVERHEATED
        else:
            state = self.transitionMap[currState]
            while not mod.isValidState(state):
                state =- 1

        if mod.isValidState(state):
            return state
        else:
            return currState
