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

class DamagePattern():
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = DamagePattern()

        return cls.instance

    def __init__(self):
        self.getDamagePatternList()

    def getDamagePatternList(self):
        patterns = eos.db.getDamagePatternList()
        if len(patterns) == 0:
            uniform = eos.types.DamagePattern(25, 25, 25, 25)
            uniform.name = "Uniform"
            eos.db.save(uniform)
            patterns.append(uniform)

        return patterns

    def getDamagePattern(self, name):
        return eos.db.getDamagePattern(name)

    def newPattern(self):
        p = eos.types.DamagePattern(0, 0, 0, 0)
        p.name = ""
        eos.db.save(p)
        return p

    def renamePattern(self, p, newName):
        p.name = newName
        eos.db.save(p)

    def deletePattern(self, p):
        eos.db.remove(p)

    def saveChanges(self, p):
        eos.db.save(p)
