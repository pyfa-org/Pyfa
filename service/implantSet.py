# =============================================================================
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
# =============================================================================

import copy

import eos.db
from service.market import Market
from eos.saveddata.implant import Implant as es_Implant
from eos.saveddata.implantSet import ImplantSet as es_ImplantSet


class ImportError(Exception):
    pass


class ImplantSets:
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = ImplantSets()

        return cls.instance

    @staticmethod
    def getImplantSetList():
        return eos.db.getImplantSetList(None)

    @staticmethod
    def getImplantSet(name):
        return eos.db.getImplantSet(name)

    @staticmethod
    def getImplants(setID):
        return eos.db.getImplantSet(setID).implants

    @staticmethod
    def addImplants(setID, *itemIDs):
        implant_set = eos.db.getImplantSet(setID)
        for itemID in itemIDs:
            implant = es_Implant(eos.db.getItem(itemID))
            implant_set.implants.makeRoom(implant)
            implant_set.implants.append(implant)
        eos.db.commit()

    @staticmethod
    def removeImplant(setID, implant):
        eos.db.getImplantSet(setID).implants.remove(implant)
        eos.db.commit()

    @staticmethod
    def newSet(name):
        implant_set = es_ImplantSet()
        implant_set.name = name
        eos.db.save(implant_set)
        return implant_set

    @staticmethod
    def renameSet(implant_set, newName):
        implant_set.name = newName
        eos.db.save(implant_set)

    @staticmethod
    def deleteSet(implant_set):
        eos.db.remove(implant_set)

    @staticmethod
    def copySet(implant_set):
        newS = copy.deepcopy(implant_set)
        eos.db.save(newS)
        return newS

    @staticmethod
    def saveChanges(implant_set):
        eos.db.save(implant_set)

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
                    current = es_ImplantSet(line[1:-1])
                    newSets.append(current)
                else:
                    item = sMkt.getItem(line)
                    current.implants.append(es_Implant(item))
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                errors += 1
                continue

        for implant_set in self.getImplantSetList():
            lookup[implant_set.name] = implant_set

        for implant_set in newSets:
            if implant_set.name in lookup:
                match = lookup[implant_set.name]
                for implant in implant_set.implants:
                    match.implants.append(es_Implant(implant.item))
            else:
                eos.db.save(implant_set)

        eos.db.commit()

        lenImports = len(newSets)
        if lenImports == 0:
            raise ImportError("No patterns found for import")
        if errors > 0:
            raise ImportError("%d sets imported from clipboard; %d errors" %
                              (lenImports, errors))

    def exportSets(self):
        patterns = self.getImplantSetList()
        patterns.sort(key=lambda p: p.name)
        return es_ImplantSet.exportSets(*patterns)
