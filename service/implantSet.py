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

import copy

import eos.db
import eos.types
from service.market import Market

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
        return eos.db.getImplantSetList(None)

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

    def newSet(self, name):
        s = eos.types.ImplantSet()
        s.name = name
        eos.db.save(s)
        return s

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

    def importSets(self, text):
        sMkt = Market.getInstance()
        lines = text.splitlines()
        newSets = []
        errors = 0
        current = None
        lookup = {}

        for i, line in enumerate(lines):
            line = line.strip()
            try:
                if line == '' or line[0] == "#":  # comments / empty string
                    continue
                if line[:1] == "[" and line[-1:] == "]":
                    current = eos.types.ImplantSet(line[1:-1])
                    newSets.append(current)
                else:
                    item = sMkt.getItem(line)
                    current.implants.append(eos.types.Implant(item))
            except:
                errors += 1
                continue

        for set in self.getImplantSetList():
            lookup[set.name] = set

        for set in newSets:
            if set.name in lookup:
                match = lookup[set.name]
                for implant in set.implants:
                    match.implants.append(eos.types.Implant(implant.item))
            else:
                eos.db.save(set)

        eos.db.commit()

        lenImports = len(newSets)
        if lenImports == 0:
            raise ImportError("No patterns found for import")
        if errors > 0:
            raise ImportError("%d sets imported from clipboard; %d errors"%(lenImports, errors))

    def exportSets(self):
        patterns = self.getImplantSetList()
        patterns.sort(key=lambda p: p.name)
        return eos.types.ImplantSet.exportSets(*patterns)
