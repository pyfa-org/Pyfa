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
from collections import OrderedDict

from sqlalchemy.orm import reconstructor

import eos.db


# Order is significant here - UI uses order as-is for built-in patterns
BUILTINS = OrderedDict([
    (-1, ('Uniform', 25, 25, 25, 25)),
    (-2, ('[Generic]EM', 1, 0, 0, 0)),
    (-3, ('[Generic]Thermal', 0, 1, 0, 0)),
    (-4, ('[Generic]Kinetic', 0, 0, 1, 0)),
    (-5, ('[Generic]Explosive', 0, 0, 0, 1)),
    (-6, ('[Frequency Crystals]|[T2] Aurora', 5, 3, 0, 0)),
    (-7, ('[Frequency Crystals]|[T2] Scorch', 9, 2, 0, 0)),
    (-8, ('[Frequency Crystals]Radio', 5, 0, 0, 0)),
    (-9, ('[Frequency Crystals]Microwave', 4, 2, 0, 0)),
    (-10, ('[Frequency Crystals]Infrared', 5, 2, 0, 0)),
    (-11, ('[Frequency Crystals]Standard', 5, 3, 0, 0)),
    (-12, ('[Frequency Crystals]Ultraviolet', 6, 3, 0, 0)),
    (-13, ('[Frequency Crystals]Xray', 6, 4, 0, 0)),
    (-14, ('[Frequency Crystals]Gamma', 7, 4, 0, 0)),
    (-15, ('[Frequency Crystals]Multifrequency', 7, 5, 0, 0)),
    (-16, ('[Frequency Crystals]|[T2] Gleam', 7, 7, 0, 0)),
    (-17, ('[Frequency Crystals]|[T2] Conflagration', 7.7, 7.7, 0, 0)),
    # Different sizes of plasma do different damage ratios, the values here
    # are average of ratios across sizes
    (-18, ('[Exotic Plasma]|[T2] Mystic', 0, 66319, 0, 33681)),
    (-19, ('[Exotic Plasma]Meson', 0, 60519, 0, 39481)),
    (-20, ('[Exotic Plasma]Baryon', 0, 59737, 0, 40263)),
    (-21, ('[Exotic Plasma]Tetryon', 0, 69208, 0, 30792)),
    (-22, ('[Exotic Plasma]|[T2] Occult', 0, 55863, 0, 44137)),
    (-23, ('[Hybrid Charges]|[T2] Spike', 0, 4, 4, 0)),
    (-24, ('[Hybrid Charges]|[T2] Null', 0, 6, 5, 0)),
    (-25, ('[Hybrid Charges]Iron', 0, 2, 3, 0)),
    (-26, ('[Hybrid Charges]Tungsten', 0, 2, 4, 0)),
    (-27, ('[Hybrid Charges]Iridium', 0, 3, 4, 0)),
    (-28, ('[Hybrid Charges]Lead', 0, 3, 5, 0)),
    (-29, ('[Hybrid Charges]Thorium', 0, 4, 5, 0)),
    (-30, ('[Hybrid Charges]Uranium', 0, 4, 6, 0)),
    (-31, ('[Hybrid Charges]Plutonium', 0, 5, 6, 0)),
    (-32, ('[Hybrid Charges]Antimatter', 0, 5, 7, 0)),
    (-33, ('[Hybrid Charges]|[T2] Javelin', 0, 8, 6, 0)),
    (-34, ('[Hybrid Charges]|[T2] Void', 0, 7.7, 7.7, 0)),
    (-35, ('[Projectile Ammo]|[T2] Tremor', 0, 0, 3, 5)),
    (-36, ('[Projectile Ammo]|[T2] Barrage', 0, 0, 5, 6)),
    (-37, ('[Projectile Ammo]Carbonized Lead', 0, 0, 4, 1)),
    (-38, ('[Projectile Ammo]Nuclear', 0, 0, 1, 4)),
    (-39, ('[Projectile Ammo]Proton', 3, 0, 2, 0)),
    (-40, ('[Projectile Ammo]Depleted Uranium', 0, 3, 2, 3)),
    (-41, ('[Projectile Ammo]Titanium Sabot', 0, 0, 6, 2)),
    (-42, ('[Projectile Ammo]EMP', 9, 0, 1, 2)),
    (-43, ('[Projectile Ammo]Phased Plasma', 0, 10, 2, 0)),
    (-44, ('[Projectile Ammo]Fusion', 0, 0, 2, 10)),
    (-45, ('[Projectile Ammo]|[T2] Quake', 0, 0, 5, 9)),
    (-46, ('[Projectile Ammo]|[T2] Hail', 0, 0, 3.3, 12.1)),
    (-47, ('[Missiles]Mjolnir', 1, 0, 0, 0)),
    (-48, ('[Missiles]Inferno', 0, 1, 0, 0)),
    (-49, ('[Missiles]Scourge', 0, 0, 1, 0)),
    (-50, ('[Missiles]Nova', 0, 0, 0, 1)),
    (-51, ('[Bombs]Electron Bomb', 6400, 0, 0, 0)),
    (-52, ('[Bombs]Scorch Bomb', 0, 6400, 0, 0)),
    (-53, ('[Bombs]Concussion Bomb', 0, 0, 6400, 0)),
    (-54, ('[Bombs]Shrapnel Bomb', 0, 0, 0, 6400)),
    # Source: ticket #2067 and #2265
    (-55, ('[NPC][Abyssal]All', 126, 427, 218, 230)),
    (-109, ('[NPC][Abyssal]Angel', 450, 72, 80, 398)),
    (-107, ('[NPC][Abyssal]Concord', 53, 559, 94, 295)),
    (-56, ('[NPC][Abyssal]Drifter', 250, 250, 250, 250)),
    (-57, ('[NPC][Abyssal]Drones', 250, 250, 250, 250)),
    (-58, ('[NPC][Abyssal]Overmind', 0, 410, 590, 0)),
    (-108, ('[NPC][Abyssal]Sansha', 569, 431, 0, 0)),
    (-59, ('[NPC][Abyssal]Seeker', 402, 402, 98, 98)),
    (-60, ('[NPC][Abyssal]Sleeper', 313, 313, 187, 187)),
    (-61, ('[NPC][Abyssal]Triglavian', 0, 615, 0, 385)),
    (-62, ('[NPC][Asteroid]Angel Cartel', 1838, 562, 2215, 3838)),
    (-63, ('[NPC][Asteroid]Blood Raiders', 5067, 4214, 0, 0)),
    (-64, ('[NPC][Asteroid]Guristas', 0, 1828, 7413, 0)),
    (-65, ('[NPC][Asteroid]Rogue Drone', 394, 666, 1090, 1687)),
    (-66, ('[NPC][Asteroid]Sanshas Nation', 5586, 4112, 0, 0)),
    (-67, ('[NPC][Asteroid]Serpentis', 0, 5373, 4813, 0)),
    (-68, ('[NPC][Burner]Cruor (Blood Raiders)', 90, 90, 0, 0)),
    (-69, ('[NPC][Burner]Dramiel (Angel)', 55, 0, 20, 96)),
    (-70, ('[NPC][Burner]Daredevil (Serpentis)', 0, 110, 154, 0)),
    (-71, ('[NPC][Burner]Succubus (Sanshas Nation)', 135, 30, 0, 0)),
    (-72, ('[NPC][Burner]Worm (Guristas)', 0, 0, 228, 0)),
    (-73, ('[NPC][Burner]Enyo', 0, 147, 147, 0)),
    (-74, ('[NPC][Burner]Hawk', 0, 0, 247, 0)),
    (-75, ('[NPC][Burner]Jaguar', 36, 0, 50, 182)),
    (-76, ('[NPC][Burner]Vengeance', 232, 0, 0, 0)),
    (-77, ('[NPC][Burner]Ashimmu (Blood Raiders)', 260, 100, 0, 0)),
    (-78, ('[NPC][Burner]Talos', 0, 413, 413, 0)),
    (-79, ('[NPC][Burner]Sentinel', 0, 75, 0, 90)),
    (-80, ('[NPC][Deadspace]Angel Cartel', 369, 533, 1395, 3302)),
    (-81, ('[NPC][Deadspace]Blood Raiders', 6040, 5052, 10, 15)),
    (-82, ('[NPC][Deadspace]Guristas', 0, 1531, 9680, 0)),
    (-83, ('[NPC][Deadspace]Rogue Drone', 276, 1071, 1069, 871)),
    (-84, ('[NPC][Deadspace]Sanshas Nation', 3009, 2237, 0, 0)),
    (-85, ('[NPC][Deadspace]Serpentis', 0, 3110, 1929, 0)),
    # Source: ticket #2067
    (-86, ('[NPC][Invasion][Triglavian Entities]Dread', 0, 417, 0, 583)),
    (-87, ('[NPC][Invasion][Triglavian Entities]Normal Subcaps', 0, 610, 0, 390)),
    (-88, ('[NPC][Invasion][Triglavian Entities]Subcaps w/missiles 0% spool up', 367, 155, 367, 112)),
    (-89, ('[NPC][Invasion][Triglavian Entities]Subcaps w/missiles 50% spool up', 291, 243, 291, 175)),
    (-90, ('[NPC][Invasion][Triglavian Entities]Subcaps w/missiles 100% spool up', 241, 301, 241, 217)),
    (-91, ('[NPC][Invasion][Retaliating Amarr Entities]Dread/Subcaps', 583, 417, 0, 0)),
    (-92, ('[NPC][Invasion][Retaliating Caldari Entities]Dread', 1000, 0, 0, 0)),
    (-93, ('[NPC][Invasion][Retaliating Caldari Entities]Subcaps', 511, 21, 29, 440)),
    (-94, ('[NPC][Invasion][Retaliating Gallente Entities]Dread/Subcaps', 0, 417, 583, 0)),
    (-95, ('[NPC][Invasion][Retaliating Minmatar Entities]Dread', 0, 0, 583, 417)),
    (-96, ('[NPC][Invasion][Retaliating Minmatar Entities]Subcaps', 302, 136, 328, 234)),
    (-97, ('[NPC][Mission]Amarr Empire', 4464, 3546, 97, 0)),
    (-98, ('[NPC][Mission]Caldari State', 0, 2139, 4867, 0)),
    (-99, ('[NPC][Mission]CONCORD', 336, 134, 212, 412)),
    (-100, ('[NPC][Mission]Gallente Federation', 9, 3712, 2758, 0)),
    (-101, ('[NPC][Mission]Khanid', 612, 483, 43, 6)),
    (-102, ('[NPC][Mission]Minmatar Republic', 1024, 388, 1655, 4285)),
    (-103, ('[NPC][Mission]Mordus Legion', 25, 262, 625, 0)),
    (-104, ('[NPC][Mission]Thukker', 0, 52, 10, 79)),
    (-105, ('[NPC]Sansha Incursion', 1682, 1347, 3678, 3678)),
    (-106, ('[NPC]Sleepers', 1472, 1472, 1384, 1384))])


class DamagePattern:

    DAMAGE_TYPES = ('em', 'thermal', 'kinetic', 'explosive')
    _builtins = None

    def __init__(self, *args, **kwargs):
        self.builtin = False
        self.update(*args, **kwargs)

    @reconstructor
    def init(self):
        self.builtin = False

    def update(self, emAmount=25, thermalAmount=25, kineticAmount=25, explosiveAmount=25):
        self.emAmount = emAmount
        self.thermalAmount = thermalAmount
        self.kineticAmount = kineticAmount
        self.explosiveAmount = explosiveAmount

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
    def getDefaultBuiltin(cls):
        if cls._builtins is None:
            cls.__generateBuiltins()
        return cls._builtins.get(-1)

    @classmethod
    def __generateBuiltins(cls):
        cls._builtins = OrderedDict()
        for id, (rawName, em, therm, kin, explo) in BUILTINS.items():
            pattern = DamagePattern(emAmount=em, thermalAmount=therm, kineticAmount=kin, explosiveAmount=explo)
            pattern.ID = id
            pattern.rawName = rawName
            pattern.builtin = True
            cls._builtins[id] = pattern

    def calculateEhp(self, fit):
        ehp = {}
        for (type, attr) in (('shield', 'shieldCapacity'), ('armor', 'armorHP'), ('hull', 'hp')):
            rawCapacity = fit.ship.getModifiedItemAttr(attr)
            ehp[type] = self.effectivify(fit, rawCapacity, type)

        return ehp

    def calculateEffectiveTank(self, fit, tankInfo):
        typeMap = {
            "passiveShield": "shield",
            "shieldRepair": "shield",
            "armorRepair": "armor",
            "armorRepairPreSpool": "armor",
            "armorRepairFullSpool": "armor",
            "hullRepair": "hull"}
        ereps = {}
        for field in tankInfo:
            if field in typeMap:
                ereps[field] = self.effectivify(fit, tankInfo[field], typeMap[field])
        return ereps

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
    def oneType(cls, damageType, amount=100):
        pattern = DamagePattern()
        pattern.update(amount if damageType == "em" else 0,
                       amount if damageType == "thermal" else 0,
                       amount if damageType == "kinetic" else 0,
                       amount if damageType == "explosive" else 0)
        return pattern

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
            lookup[pattern.rawName] = pattern

        for line in lines:
            try:
                if line.strip()[0] == "#":  # comments
                    continue
                line = line.split('#', 1)[0]  # allows for comments
                type, data = line.rsplit('=', 1)
                type, data = type.strip(), data.split(',')
            except (KeyboardInterrupt, SystemExit):
                raise
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
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    continue

            if len(fields) == 4:  # Avoid possible blank lines
                if name.strip() in lookup:
                    pattern = lookup[name.strip()]
                    pattern.update(**fields)
                    eos.db.save(pattern)
                else:
                    pattern = DamagePattern(**fields)
                    pattern.rawName = name.strip()
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
            out += cls.EXPORT_FORMAT % (dp.rawName, dp.emAmount, dp.thermalAmount, dp.kineticAmount, dp.explosiveAmount)

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
        categories = []
        remainingName = self.rawName.strip() if self.rawName else ''
        while True:
            start, end = remainingName.find('['), remainingName.find(']')
            if start == -1 or end == -1:
                return categories, remainingName
            splitter = remainingName.find('|')
            if splitter != -1 and splitter == start - 1:
                return categories, remainingName[1:]
            categories.append(remainingName[start + 1:end])
            remainingName = remainingName[end + 1:].strip()

    def __deepcopy__(self, memo):
        p = DamagePattern(self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount)
        p.rawName = "%s copy" % self.rawName
        return p
