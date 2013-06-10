#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import re

class DamagePattern(object):
    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, emAmount = 25, thermalAmount = 25, kineticAmount = 25, explosiveAmount = 25):
        self.emAmount = emAmount
        self.thermalAmount = thermalAmount
        self.kineticAmount = kineticAmount
        self.explosiveAmount = explosiveAmount

    def calculateEhp(self, fit):
        ehp = {}
        for (type, attr) in (('shield', 'shieldCapacity'), ('armor', 'armorHP'), ('hull', 'hp')):
            rawCapacity = fit.ship.getModifiedItemAttr(attr)
            ehp[type] = self.effectivify(fit, rawCapacity, type)

        return ehp

    def calculateEffectiveTank(self, fit, tankInfo):
        ehps = {}
        passiveShield = fit.calculateShieldRecharge()
        ehps["passiveShield"] = self.effectivify(fit, passiveShield, "shield")
        for type in ("shield", "armor", "hull"):
            ehps["%sRepair" % type] = self.effectivify(fit, tankInfo["%sRepair" % type], type)

        return ehps

    def effectivify(self, fit, amount, type):
        type = type if type != "hull" else ""
        totalDamage = sum((self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount))
        specificDivider = 0
        for damageType in self.DAMAGE_TYPES:
            #Compose an attribute name, then make sure the first letter is NOT capitalized
            attrName = "%s%sDamageResonance" % (type, damageType.capitalize())
            attrName = attrName[0].lower() + attrName[1:]

            resonance = fit.ship.getModifiedItemAttr(attrName)
            damage = getattr(self, "%sAmount" % damageType)

            specificDivider += damage / float(totalDamage or 1) * resonance

        return amount / (specificDivider or 1)

    importMap = {"em": "em",
                 "therm": "thermal",
                 "kin": "kinetic",
                 "exp": "explosive"}
    @classmethod
    def importPatterns(cls, text):
        lines = re.split('[\n\r]+', text)
        patterns = []
        for line in lines:
            line = line.split('#',1)[0] # allows for comments
            name, data = line.rsplit('=',1)
            name, data = name.strip(), ''.join(data.split()) # whitespace

            fields = {}
            for entry in data.split(','):
                key, val = entry.split(':')
                fields["%sAmount" % cls.importMap[key.lower()]] = float(val)

            pattern = DamagePattern(**fields)
            pattern.name = name
            patterns.append(pattern)

        return patterns

    EXPORT_FORMAT = "%s = EM:%d, Therm:%d, Kin:%d, Exp:%d\n"
    @classmethod
    def exportPatterns(cls, *patterns):
        out = ""
        for dp in patterns:
            out += cls.EXPORT_FORMAT % (dp.name, dp.emAmount, dp.thermalAmount, dp.kineticAmount, dp.explosiveAmount)

        return out.strip()

    def __deepcopy__(self, memo):
        p = DamagePattern(self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount)
        p.name = "%s copy" % self.name
        return p
