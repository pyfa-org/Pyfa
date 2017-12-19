# ===============================================================================
# Copyright (C) 2014 Ryan Holmes
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
from logbook import Logger

pyfalog = Logger(__name__)


class TargetResists(object):
    # also determined import/export order - VERY IMPORTANT
    DAMAGE_TYPES = ("em", "thermal", "kinetic", "explosive")
    ATTRIBUTES = ("signatureRadius", "maxVelocity")

    def __init__(self, emAmount=0, thermalAmount=0, kineticAmount=0, explosiveAmount=0, signatureRadius=0, maxVelocity=0):
        self.emAmount = emAmount
        self.thermalAmount = thermalAmount
        self.kineticAmount = kineticAmount
        self.explosiveAmount = explosiveAmount
        self.signatureRadius = signatureRadius
        self.maxVelocity = maxVelocity

    def getAttribute(self, attr):
        if attr in ("emDamageResonance", "armorEmDamageResonance", "shieldEmDamageResonance"):
            attr = "emAmount"
        elif attr in ("thermalDamageResonance", "armorThermalDamageResonance", "shieldThermalDamageResonance"):
            attr = "thermalAmount"
        elif attr in ("kineticDamageResonance", "armorKineticDamageResonance", "shieldKineticDamageResonance"):
            attr = "kineticAmount"
        elif attr in ("explosiveDamageResonance", "armorExplosiveDamageResonance", "shieldExplosiveDamageResonance"):
            attr = "explosiveAmount"
        return getattr(self, attr, None)

    @classmethod
    def importPatterns(cls, text):
        lines = re.split('[\n\r]+', text)
        patterns = []
        numPatterns = 0
        for line in lines:
            try:
                if line.strip()[0] == "#":  # comments
                    continue
                line = line.split('#', 1)[0]  # allows for comments
                type, data = line.rsplit('=', 1)
                type, data = type.strip(), data.split(',')
            except:
                pyfalog.warning("Data isn't in correct format, continue to next line.")
                continue

            if type != "TargetResists":
                continue

            numPatterns += 1
            name, data = data[0], data[1:7]
            fields = {}

            for index, val in enumerate(data):
                if index < 4:
                    val = float(val)
                    try:
                        assert 0 <= val <= 100
                        fields["%sAmount" % cls.DAMAGE_TYPES[index]] = val / 100
                    except:
                        pyfalog.warning("Caught unhandled exception in import patterns.")
                        continue
                elif index < 6:
                    val = float(val)
                    try:
                        assert 0 <= val
                        fields[cls.ATTRIBUTES[index - 4]] = val
                    except:
                        pyfalog.warning("Caught unhandled exception in import patterns.")
                        continue

            if len(fields) >= 4 and len(fields) <= 6:  # Avoid possible blank lines
                pattern = TargetResists(**fields)
                pattern.name = name.strip()
                patterns.append(pattern)

        return patterns, numPatterns

    EXPORT_FORMAT = "TargetResists = %s,%.1f,%.1f,%.1f,%.1f,%.1f,%.1f\n"

    @classmethod
    def exportPatterns(cls, *patterns):
        out = "# Exported from pyfa\n#\n"
        out += "# Values are in following format:\n"
        out += "# TargetResists = [name],[EM %],[Thermal %],[Kinetic %],[Explosive %],[Signature Radius],[Max Velocity]\n\n"
        for dp in patterns:
            out += cls.EXPORT_FORMAT % (
                dp.name,
                dp.emAmount * 100,
                dp.thermalAmount * 100,
                dp.kineticAmount * 100,
                dp.explosiveAmount * 100,
                dp.signatureRadius,
                dp.maxVelocity
            )

        return out.strip()

    def __deepcopy__(self, memo):
        p = TargetResists(self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount, self.signatureRadius, self.maxVelocity)
        p.name = "%s copy" % self.name
        return p
