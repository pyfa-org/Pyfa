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
import copy

class ImportError(Exception):
    pass

class DamagePattern():
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = DamagePattern()

        return cls.instance

    def __init__(self):
        uniform = eos.db.getDamagePattern("Uniform")
        if uniform is None:
            uniform = eos.types.DamagePattern(25, 25, 25, 25)
            uniform.name = "Uniform"
            eos.db.save(uniform)

    def getDamagePatternList(self):
        return eos.db.getDamagePatternList()

    def getDamagePattern(self, name):
        return eos.db.getDamagePattern(name)

    def newPattern(self):
        p = eos.types.DamagePattern(0, 0, 0, 0)
        p.name = ""
        return p

    def renamePattern(self, p, newName):
        p.name = newName
        eos.db.save(p)

    def deletePattern(self, p):
        eos.db.remove(p)

    def copyPattern(self, p):
        newP = copy.deepcopy(p)
        eos.db.save(newP)
        return newP

    def saveChanges(self, p):
        eos.db.save(p)

    def importPatterns(self, text):
        lookup = {}
        current = self.getDamagePatternList()
        for pattern in current:
            lookup[pattern.name] = pattern

        imports, num = eos.types.DamagePattern.importPatterns(text)
        for pattern in imports:
            if pattern.name in lookup:
                match = lookup[pattern.name]
                match.__dict__.update(pattern.__dict__)
            else:
                eos.db.save(pattern)
        eos.db.commit()

        lenImports = len(imports)
        if lenImports == 0:
            raise ImportError("No patterns found for import")
        if lenImports != num:
            raise ImportError("%d patterns imported from clipboard; %d had errors"%(num, num-lenImports))

    def exportPatterns(self):
        patterns = self.getDamagePatternList()
        for i in xrange(len(patterns) - 1, -1, -1):
            if patterns[i].name in ("Uniform", "Selected Ammo"):
                del patterns[i]

        patterns.sort(key=lambda p: p.name)
        return eos.types.DamagePattern.exportPatterns(*patterns)

