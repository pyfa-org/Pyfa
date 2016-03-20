#===============================================================================
# Copyright (C) 2016 Ryan Holmes
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
import copy

class ImportError(Exception):
    pass

class ImplantSets():
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = ImplantSets()

        return cls.instance

    def getImplantSetList(self):
        return eos.db.getImplantSet(None)

    def getImplantSet(self, name):
        return eos.db.getImplantSet(name)

    def getImplants(self, setID):
        set = eos.db.getImplantSet(setID)
        return set.implants

    def addImplant(self, setID, itemID):
        set = eos.db.getImplantSet(setID)
        implant = eos.types.Implant(eos.db.getItem(itemID))
        set.implants.append(implant)
        eos.db.commit()

    def removeImplant(self, setID, implant):
        set = eos.db.getImplantSet(setID)
        set.implants.remove(implant)
        eos.db.commit()

    def newSet(self):
        p = eos.types.ImplantSet()
        p.name = ""
        return p

    def renameSet(self, s, newName):
        s.name = newName
        eos.db.save(s)

    def deleteSet(self, s):
        eos.db.remove(s)

    def copySet(self, s):
        newS = copy.deepcopy(s)
        eos.db.save(newS)
        return newS

    def saveChanges(self, s):
        eos.db.save(s)
