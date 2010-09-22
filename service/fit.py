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
from eos.types import State
import copy

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

    def newFit(self, shipID, name):
        fit = eos.types.Fit()
        fit.ship = eos.types.Ship(eos.db.getItem(shipID))
        fit.name = name
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
        fit.implants.remove(booster)
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

    def changeChar(self, fitID, charID):
        if fitID is None or charID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.character = eos.db.getCharacter(charID)
        fit.clear()
        fit.calculateModifiedAttributes()
