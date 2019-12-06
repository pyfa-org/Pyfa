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

import math
import re
from collections import OrderedDict

from logbook import Logger
from sqlalchemy.orm import reconstructor

import eos.db


pyfalog = Logger(__name__)


BUILTINS = OrderedDict([
    # 0 is taken by ideal target profile, composed manually in one of TargetProfile methods
    (-1, ('Uniform (25%)', 0.25, 0.25, 0.25, 0.25)),
    (-2, ('Uniform (50%)', 0.50, 0.50, 0.50, 0.50)),
    (-3, ('Uniform (75%)', 0.75, 0.75, 0.75, 0.75)),
    (-4, ('Uniform (90%)', 0.90, 0.90, 0.90, 0.90)),
    (-5, ('[T1 Resist]Shield', 0.0, 0.20, 0.40, 0.50)),
    (-6, ('[T1 Resist]Armor', 0.50, 0.45, 0.25, 0.10)),
    (-7, ('[T1 Resist]Hull', 0.33, 0.33, 0.33, 0.33)),
    (-8, ('[T1 Resist]Shield (+T2 DCU)', 0.125, 0.30, 0.475, 0.562)),
    (-9, ('[T1 Resist]Armor (+T2 DCU)', 0.575, 0.532, 0.363, 0.235)),
    (-10, ('[T1 Resist]Hull (+T2 DCU)', 0.598, 0.598, 0.598, 0.598)),
    (-11, ('[T2 Resist]Amarr (Shield)', 0.0, 0.20, 0.70, 0.875)),
    (-12, ('[T2 Resist]Amarr (Armor)', 0.50, 0.35, 0.625, 0.80)),
    (-13, ('[T2 Resist]Caldari (Shield)', 0.20, 0.84, 0.76, 0.60)),
    (-14, ('[T2 Resist]Caldari (Armor)', 0.50, 0.8625, 0.625, 0.10)),
    (-15, ('[T2 Resist]Gallente (Shield)', 0.0, 0.60, 0.85, 0.50)),
    (-16, ('[T2 Resist]Gallente (Armor)', 0.50, 0.675, 0.8375, 0.10)),
    (-17, ('[T2 Resist]Minmatar (Shield)', 0.75, 0.60, 0.40, 0.50)),
    (-18, ('[T2 Resist]Minmatar (Armor)', 0.90, 0.675, 0.25, 0.10)),
    (-19, ('[NPC][Asteroid]Angel Cartel', 0.54, 0.42, 0.37, 0.32)),
    (-20, ('[NPC][Asteroid]Blood Raiders', 0.34, 0.39, 0.45, 0.52)),
    (-21, ('[NPC][Asteroid]Guristas', 0.55, 0.35, 0.3, 0.48)),
    (-22, ('[NPC][Asteroid]Rogue Drones', 0.35, 0.38, 0.44, 0.49)),
    (-23, ('[NPC][Asteroid]Sanshas Nation', 0.35, 0.4, 0.47, 0.53)),
    (-24, ('[NPC][Asteroid]Serpentis', 0.49, 0.38, 0.29, 0.51)),
    (-25, ('[NPC][Deadspace]Angel Cartel', 0.59, 0.48, 0.4, 0.32)),
    (-26, ('[NPC][Deadspace]Blood Raiders', 0.31, 0.39, 0.47, 0.56)),
    (-27, ('[NPC][Deadspace]Guristas', 0.57, 0.39, 0.31, 0.5)),
    (-28, ('[NPC][Deadspace]Rogue Drones', 0.42, 0.42, 0.47, 0.49)),
    (-29, ('[NPC][Deadspace]Sanshas Nation', 0.31, 0.39, 0.47, 0.56)),
    (-30, ('[NPC][Deadspace]Serpentis', 0.49, 0.38, 0.29, 0.56)),
    (-31, ('[NPC][Mission]Amarr Empire', 0.34, 0.38, 0.42, 0.46)),
    (-32, ('[NPC][Mission]Caldari State', 0.51, 0.38, 0.3, 0.51)),
    (-33, ('[NPC][Mission]CONCORD', 0.47, 0.46, 0.47, 0.47)),
    (-34, ('[NPC][Mission]Gallente Federation', 0.51, 0.38, 0.31, 0.52)),
    (-35, ('[NPC][Mission]Khanid', 0.51, 0.42, 0.36, 0.4)),
    (-36, ('[NPC][Mission]Minmatar Republic', 0.51, 0.46, 0.41, 0.35)),
    (-37, ('[NPC][Mission]Mordus Legion', 0.32, 0.48, 0.4, 0.62)),
    (-38, ('[NPC][Other]Sleeper', 0.61, 0.61, 0.61, 0.61)),
    (-39, ('[NPC][Other]Sansha Incursion', 0.65, 0.63, 0.64, 0.65)),
    (-40, ('[NPC][Burner]Cruor (Blood Raiders)', 0.8, 0.73, 0.69, 0.67)),
    (-41, ('[NPC][Burner]Dramiel (Angel)', 0.35, 0.48, 0.61, 0.68)),
    (-42, ('[NPC][Burner]Daredevil (Serpentis)', 0.69, 0.59, 0.59, 0.43)),
    (-43, ('[NPC][Burner]Succubus (Sanshas Nation)', 0.35, 0.48, 0.61, 0.68)),
    (-44, ('[NPC][Burner]Worm (Guristas)', 0.48, 0.58, 0.69, 0.74)),
    (-45, ('[NPC][Burner]Enyo', 0.58, 0.72, 0.86, 0.24)),
    (-46, ('[NPC][Burner]Hawk', 0.3, 0.86, 0.79, 0.65)),
    (-47, ('[NPC][Burner]Jaguar', 0.78, 0.65, 0.48, 0.56)),
    (-48, ('[NPC][Burner]Vengeance', 0.66, 0.56, 0.75, 0.86)),
    (-49, ('[NPC][Burner]Ashimmu (Blood Raiders)', 0.8, 0.76, 0.68, 0.7)),
    (-50, ('[NPC][Burner]Talos', 0.68, 0.59, 0.59, 0.43)),
    (-51, ('[NPC][Burner]Sentinel', 0.58, 0.45, 0.52, 0.66)),
    # Source: ticket #2067
    (-52, ('[NPC][Invasion]Invading Precursor Entities', 0.46, 0.39, 0.48, 0.42)),
    (-53, ('[NPC][Invasion]Retaliating Amarr Entities', 0.36, 0.31, 0.44, 0.60)),
    (-54, ('[NPC][Invasion]Retaliating Caldari Entities', 0.28, 0.61, 0.48, 0.39)),
    (-55, ('[NPC][Invasion]Retaliating Gallente Entities', 0.36, 0.39, 0.56, 0.50)),
    (-56, ('[NPC][Invasion]Retaliating Minmatar Entities', 0.62, 0.42, 0.35, 0.40))])


class TargetProfile:

    # also determined import/export order - VERY IMPORTANT
    DAMAGE_TYPES = ('em', 'thermal', 'kinetic', 'explosive')
    _idealTarget = None
    _builtins = None

    def __init__(self, *args, **kwargs):
        self.builtin = False
        self.update(*args, **kwargs)

    @reconstructor
    def init(self):
        self.builtin = False

    def update(self, emAmount=0, thermalAmount=0, kineticAmount=0, explosiveAmount=0, maxVelocity=None, signatureRadius=None, radius=None):
        self.emAmount = emAmount
        self.thermalAmount = thermalAmount
        self.kineticAmount = kineticAmount
        self.explosiveAmount = explosiveAmount
        self._maxVelocity = maxVelocity
        self._signatureRadius = signatureRadius
        self._radius = radius

    @classmethod
    def getBuiltinList(cls):
        if cls._builtins is None:
            cls.__generateBuiltins()
        return list(cls._builtins.values())

    @classmethod
    def getBuiltinById(cls, id):
        if cls._builtins is None:
            cls.__generateBuiltins()
        return cls._builtins.get(id)

    @classmethod
    def __generateBuiltins(cls):
        cls._builtins = OrderedDict()
        for id, data in BUILTINS.items():
            rawName = data[0]
            data = data[1:]
            profile = TargetProfile(*data)
            profile.ID = id
            profile.rawName = rawName
            profile.builtin = True
            cls._builtins[id] = profile

    @classmethod
    def getIdeal(cls):
        if cls._idealTarget is None:
            cls._idealTarget = cls(
                emAmount=0,
                thermalAmount=0,
                kineticAmount=0,
                explosiveAmount=0,
                maxVelocity=0,
                signatureRadius=None,
                radius=0)
            cls._idealTarget.rawName = 'Ideal Target'
            cls._idealTarget.ID = 0
            cls._idealTarget.builtin = True
        return cls._idealTarget

    @property
    def maxVelocity(self):
        return self._maxVelocity or 0

    @maxVelocity.setter
    def maxVelocity(self, val):
        self._maxVelocity = val

    @property
    def signatureRadius(self):
        if self._signatureRadius is None or self._signatureRadius == -1:
            return math.inf
        return self._signatureRadius

    @signatureRadius.setter
    def signatureRadius(self, val):
        if val is not None and math.isinf(val):
            val = None
        self._signatureRadius = val

    @property
    def radius(self):
        return self._radius or 0

    @radius.setter
    def radius(self, val):
        self._radius = val

    @classmethod
    def importPatterns(cls, text):
        lines = re.split('[\n\r]+', text)
        patterns = []
        numPatterns = 0

        # When we import damage profiles, we create new ones and update old ones. To do this, get a list of current
        # patterns to allow lookup
        lookup = {}
        current = eos.db.getTargetProfileList()
        for pattern in current:
            lookup[pattern.rawName] = pattern

        for line in lines:
            try:
                if line.strip()[0] == "#":  # comments
                    continue
                line = line.split('#', 1)[0]  # allows for comments
                type, data = line.rsplit('=', 1)
                type, data = type.strip(), [d.strip() for d in data.split(',')]
            except:
                pyfalog.warning("Data isn't in correct format, continue to next line.")
                continue

            if type not in ("TargetProfile", "TargetResists"):
                continue

            numPatterns += 1
            name, dataRes, dataMisc = data[0], data[1:5], data[5:8]
            fields = {}

            for index, val in enumerate(dataRes):
                val = float(val) if val else 0
                if math.isinf(val):
                    val = 0
                try:
                    assert 0 <= val <= 100
                    fields["%sAmount" % cls.DAMAGE_TYPES[index]] = val / 100
                except:
                    pyfalog.warning("Caught unhandled exception in import patterns.")
                    continue

            if len(dataMisc) == 3:
                for index, val in enumerate(dataMisc):
                    try:
                        fieldName = ("maxVelocity", "signatureRadius", "radius")[index]
                    except IndexError:
                        break
                    val = float(val) if val else 0
                    if fieldName != "signatureRadius" and math.isinf(val):
                        val = 0
                    fields[fieldName] = val

            if len(fields) in (4, 7):  # Avoid possible blank lines
                if name.strip() in lookup:
                    pattern = lookup[name.strip()]
                    pattern.update(**fields)
                    eos.db.save(pattern)
                else:
                    pattern = TargetProfile(**fields)
                    pattern.rawName = name.strip()
                    eos.db.save(pattern)
                patterns.append(pattern)

        eos.db.commit()

        return patterns, numPatterns

    EXPORT_FORMAT = "TargetProfile = %s,%.1f,%.1f,%.1f,%.1f,%.1f,%.1f,%.1f\n"

    @classmethod
    def exportPatterns(cls, *patterns):
        out = "# Exported from pyfa\n#\n"
        out += "# Values are in following format:\n"
        out += "# TargetProfile = [name],[EM %],[Thermal %],[Kinetic %],[Explosive %],[Max velocity m/s],[Signature radius m],[Radius m]\n\n"
        for dp in patterns:
            out += cls.EXPORT_FORMAT % (
                dp.rawName,
                dp.emAmount * 100,
                dp.thermalAmount * 100,
                dp.kineticAmount * 100,
                dp.explosiveAmount * 100,
                dp.maxVelocity,
                dp.signatureRadius,
                dp.radius
            )

        return out.strip()

    @property
    def name(self):
        return self.rawName

    @property
    def fullName(self):
        categories, tail = self.__parseRawName()
        return '{}{}'.format(''.join('[{}]'.format(c) for c in categories), tail)

    @property
    def shortName(self):
        return self.__parseRawName()[1]

    @property
    def hierarchy(self):
        return self.__parseRawName()[0]

    def __parseRawName(self):
        hierarchy = []
        remainingName = self.rawName.strip() if self.rawName else ''
        while True:
            start, end = remainingName.find('['), remainingName.find(']')
            if start == -1 or end == -1:
                return hierarchy, remainingName
            splitter = remainingName.find('|')
            if splitter != -1 and splitter == start - 1:
                return hierarchy, remainingName[1:]
            hierarchy.append(remainingName[start + 1:end])
            remainingName = remainingName[end + 1:].strip()

    def __deepcopy__(self, memo):
        p = TargetProfile(
            self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount,
            self._maxVelocity, self._signatureRadius, self._radius)
        p.rawName = "%s copy" % self.rawName
        return p
