# =============================================================================
# Copyright (C) 2014 Ryan Holmes
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

from eos import db
from eos.saveddata.targetResists import TargetResists as es_TargetResists


class ImportError(Exception):
    pass


class TargetResists(object):
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = TargetResists()

        return cls.instance

    @staticmethod
    def getTargetResistsList():
        return db.getTargetResistsList()

    @staticmethod
    def getTargetResists(name):
        return db.getTargetResists(name)

    @staticmethod
    def newPattern(name):
        p = es_TargetResists(0.0, 0.0, 0.0, 0.0)
        p.name = name
        db.save(p)
        return p

    @staticmethod
    def renamePattern(p, newName):
        p.name = newName
        db.save(p)

    @staticmethod
    def deletePattern(p):
        db.remove(p)

    @staticmethod
    def copyPattern(p):
        newP = copy.deepcopy(p)
        db.save(newP)
        return newP

    @staticmethod
    def saveChanges(p):
        db.save(p)

    def importPatterns(self, text):
        imports, num = es_TargetResists.importPatterns(text)
        lenImports = len(imports)

        if lenImports == 0:
            raise ImportError("No patterns found for import")
        if lenImports != num:
            raise ImportError("%d patterns imported from clipboard; %d had errors" % (num, num - lenImports))

    def exportPatterns(self):
        patterns = self.getTargetResistsList()
        patterns.sort(key=lambda p: p.name)
        return es_TargetResists.exportPatterns(*patterns)
