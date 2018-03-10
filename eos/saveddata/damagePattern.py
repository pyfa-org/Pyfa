# ===============================================================================
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
# ===============================================================================

import re
import eos.db


class DamagePattern(object):
    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def update(self, emAmount=25, thermalAmount=25, kineticAmount=25, explosiveAmount=25):
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
            # Compose an attribute name, then make sure the first letter is NOT capitalized
            attrName = "%s%sDamageResonance" % (type, damageType.capitalize())
            attrName = attrName[0].lower() + attrName[1:]

            resonance = fit.ship.getModifiedItemAttr(attrName)
            damage = getattr(self, "%sAmount" % damageType)

            specificDivider += damage / float(totalDamage or 1) * resonance

        return amount / (specificDivider or 1)

    importMap = {
        "em"   : "em",
        "therm": "thermal",
        "kin"  : "kinetic",
        "exp"  : "explosive"
    }

    @classmethod
    def importPatterns(cls, text):
        lines = re.split('[\n\r]+', text)
        patterns = []
        numPatterns = 0

        # When we import damage profiles, we create new ones and update old ones. To do this, get a list of current
        # patterns to allow lookup
        lookup = {}
        current = eos.db.getDamagePatternList()
        for pattern in current:
            lookup[pattern.name] = pattern

        for line in lines:
            try:
                if line.strip()[0] == "#":  # comments
                    continue
                line = line.split('#', 1)[0]  # allows for comments
                type, data = line.rsplit('=', 1)
                type, data = type.strip(), data.split(',')
            except:
                # Data isn't in correct format, continue to next line
                continue

            if type != "DamageProfile":
                continue

            numPatterns += 1
            name, data = data[0], data[1:5]
            fields = {}

            for index, val in enumerate(data):
                try:
                    fields["%sAmount" % cls.DAMAGE_TYPES[index]] = int(val)
                except:
                    continue

            if len(fields) == 4:  # Avoid possible blank lines
                if name.strip() in lookup:
                    pattern = lookup[name.strip()]
                    pattern.update(**fields)
                    eos.db.save(pattern)
                else:
                    pattern = DamagePattern(**fields)
                    pattern.name = name.strip()
                    eos.db.save(pattern)
                patterns.append(pattern)

        eos.db.commit()

        return patterns, numPatterns

    EXPORT_FORMAT = "DamageProfile = %s,%d,%d,%d,%d\n"

    @classmethod
    def exportPatterns(cls, *patterns):
        out = "# Exported from pyfa\n#\n"
        out += "# Values are in following format:\n"
        out += "# DamageProfile = [name],[EM amount],[Thermal amount],[Kinetic amount],[Explosive amount]\n\n"
        for dp in patterns:
            out += cls.EXPORT_FORMAT % (dp.name, dp.emAmount, dp.thermalAmount, dp.kineticAmount, dp.explosiveAmount)

        return out.strip()

    def __deepcopy__(self, memo):
        p = DamagePattern(self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount)
        p.name = "%s copy" % self.name
        return p
