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
        return fit

    def appendModule(self, fitID, itemID):
        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        if item.category.name == "Module":
            m = eos.types.Module(item)
            if m.isValidState(State.ACTIVE):
                m.state = State.ACTIVE

            if m.fits(fit):
                fit.modules.append(m)

            eos.db.commit()
            fit.clear()
            fit.calculateModifiedAttributes()
        return True

    def removeModule(self, fitID, position):
        fit = eos.db.getFit(fitID)
        if fit.modules[position].isEmpty:
            return False

        fit.modules.toDummy(position)
        eos.db.commit()
        fit.clear()
        fit.calculateModifiedAttributes()
        return True

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