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
from eos.types import Fleet as Fleet_
import copy

class Fleet(object):
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Fleet()

        return cls.instance

    def __init__(self):
        pass

    def getFleetList(self):
        fleetList = []
        fleets = eos.db.getFleetList()
        for fleet in fleets:
            fleetList.append((fleet.ID, fleet.name, fleet.count()))

        return fleetList

    def getFleet(self, ID):
        f = eos.db.getFleet(ID)
        return f

    def addFleet(self):
        f = Fleet_()
        eos.db.save(f)
        return f

    def renameFleet(self, fleet, newName):
        fleet.name = newName
        eos.db.commit()

    def copyFleet(self, fleet):
        newFleet = copy.deepcopy(fleet)
        eos.db.save(newFleet)
        return newFleet

    def deleteFleet(self, fleet):
        eos.db.remove(fleet)

