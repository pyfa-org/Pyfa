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
        eos.db.saveddata_session.add(fit)
        eos.db.saveddata_session.flush()
        fit.calculateModifiedAttributes()
        return fit.ID

    def renameFit(self, fitID, newName):
        fit = eos.db.getFit(fitID)
        fit.name = newName
        eos.db.saveddata_session.flush()

    def deleteFit(self, fitID):
        fit = eos.db.getFit(fitID)
        eos.db.saveddata_session.delete(fit)
        eos.db.saveddata_session.flush()

    def copyFit(self, fitID):
        fit = eos.db.getFit(fitID)
        newFit = copy.deepcopy(fit)
        eos.db.saveddata_session.add(newFit)
        eos.db.saveddata_session.flush()
        return newFit.ID

    def getFit(self, fitID):
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        fit.fill()
        eos.db.saveddata_session.flush()
        return fit

    def appendModule(self, fitID, itemID):
        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        if item.group.category.name == "Module":
            m = eos.types.Module(item)
            if m.isValidState(State.ACTIVE):
                m.state = State.ACTIVE

            if m.fits(fit):
                fit.modules.append(m)

        eos.db.saveddata_session.flush()
        fit.clear()
        fit.calculateModifiedAttributes()
        return fit

    def removeModule(self, fitID, position):
        fit = eos.db.getFit(fitID)
        fit.modules.toDummy(position)
        eos.db.saveddata_session.flush()
        fit.clear()
        fit.calculateModifiedAttributes()
        return fit
