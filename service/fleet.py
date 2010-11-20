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
from eos.types import Fit, Ship, Character
from eos.types import Fleet as Fleet_

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
            fleetList.append(fleet.ID, fleet.name, fleet.count())

        return fleetList

    def getFleet(self, ID):
        f = Fleet_()
        f.name = "Test"
        f.leader = Fit()
        f.leader.name = "FC"
        f.leader.ship = Ship(eos.db.getItem("Damnation"))
        f.character = Character("Moo")
        f.calculateModifiedAttributes()
        return f
