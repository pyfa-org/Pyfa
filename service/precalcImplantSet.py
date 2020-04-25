# =============================================================================
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
# =============================================================================


import eos.db
from eos.db.saveddata.implant import Implant

from service.market import Market


class PrecalcedImplantSets:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = PrecalcedImplantSets()
        return cls.instance

    @staticmethod
    def getImplantSets():
        return eos.db.getAllImplantSets()

    @staticmethod
    def getStructuredSets():
        structured = {}
        for implantSet in PrecalcedImplantSets.getImplantSets():
            structured.setdefault(implantSet.setName, {})[implantSet.gradeName] = implantSet.implants
        return structured

    @staticmethod
    def stringToImplants(string):
        sMkt = Market.getInstance()
        implants = []
        for typeID in (int(tid) for tid in string.split(',')):
            item = sMkt.getItem(typeID)
            if item is None:
                continue
            try:
                implant = Implant(item)
            except ValueError:
                continue
            implants.append(implant)
        return implants


