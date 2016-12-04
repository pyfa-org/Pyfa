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

import copy

import eos.db
from eos.saveddata.damagePattern import DamagePattern as es_DamagePattern


class DamagePattern():
    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = DamagePattern()

        return cls.instance

    def getDamagePatternList(self):
        return eos.db.getDamagePatternList()

    def getDamagePattern(self, name):
        return eos.db.getDamagePattern(name)

    def newPattern(self, name):
        p = es_DamagePattern(0, 0, 0, 0)
        p.name = name
        eds_queries.save(p)
        return p

    def renamePattern(self, p, newName):
        p.name = newName
        eds_queries.save(p)

    def deletePattern(self, p):
        eos.db.remove(p)

    def copyPattern(self, p):
        newP = copy.deepcopy(p)
        eds_queries.save(newP)
        return newP

    def saveChanges(self, p):
        eds_queries.save(p)

    def importPatterns(self, text):
        lookup = {}
        current = self.getDamagePatternList()
        for pattern in current:
            lookup[pattern.name] = pattern

        imports, num = es_DamagePattern.importPatterns(text)
        for pattern in imports:
            if pattern.name in lookup:
                match = lookup[pattern.name]
                match.__dict__.update(pattern.__dict__)
            else:
                eds_queries.save(pattern)
        eds_queries.commit()

        lenImports = len(imports)
        if lenImports == 0:
            raise ImportError("No patterns found for import")
        if lenImports != num:
            raise ImportError("%d patterns imported from clipboard; %d had errors" % (num, num - lenImports))

    def exportPatterns(self):
        patterns = self.getDamagePatternList()
        for i in xrange(len(patterns) - 1, -1, -1):
            if patterns[i].name in ("Uniform", "Selected Ammo"):
                del patterns[i]

        patterns.sort(key=lambda p: p.name)
        return es_DamagePattern.exportPatterns(*patterns)
