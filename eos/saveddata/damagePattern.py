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


def _t(x):
    return x


def _c(x):
    return '[' + x + ']'


# Order is significant here - UI uses order as-is for built-in patterns
BUILTINS = OrderedDict([
    (-1, (_t('Uniform'), 25, 25, 25, 25)),
    (-2, (_c(_t('Generic')) + _t('EM'), 1, 0, 0, 0)),
    (-3, (_c(_t('Generic')) + _t('Thermal'), 0, 1, 0, 0)),
    (-4, (_c(_t('Generic')) + _t('Kinetic'), 0, 0, 1, 0)),
    (-5, (_c(_t('Generic')) + _t('Explosive'), 0, 0, 0, 1)),
    (-6, (_c(_t('Frequency Crystals')) + '|' + _t('[T2] Aurora'), 5, 3, 0, 0)),
    (-7, (_c(_t('Frequency Crystals')) + '|' + _t('[T2] Scorch'), 9, 2, 0, 0)),
    (-8, (_c(_t('Frequency Crystals')) + _t('Radio'), 5, 0, 0, 0)),
    (-9, (_c(_t('Frequency Crystals')) + _t('Microwave'), 4, 2, 0, 0)),
    (-10, (_c(_t('Frequency Crystals')) + _t('Infrared'), 5, 2, 0, 0)),
    (-11, (_c(_t('Frequency Crystals')) + _t('Standard'), 5, 3, 0, 0)),
    (-12, (_c(_t('Frequency Crystals')) + _t('Ultraviolet'), 6, 3, 0, 0)),
    (-13, (_c(_t('Frequency Crystals')) + _t('Xray'), 6, 4, 0, 0)),
    (-14, (_c(_t('Frequency Crystals')) + _t('Gamma'), 7, 4, 0, 0)),
    (-15, (_c(_t('Frequency Crystals')) + _t('Multifrequency'), 7, 5, 0, 0)),
    (-16, (_c(_t('Frequency Crystals')) + '|' + _t('[T2] Gleam'), 7, 7, 0, 0)),
    (-17, (_c(_t('Frequency Crystals')) + '|' + _t('[T2] Conflagration'), 7.7, 7.7, 0, 0)),
    # Different sizes of plasma do different damage ratios, the values here
    # are average of ratios across sizes
    (-18, (_c(_t('Exotic Plasma')) + '|' + _t('[T2] Mystic'), 0, 66319, 0, 33681)),
    (-19, (_c(_t('Exotic Plasma')) + _t('Meson'), 0, 60519, 0, 39481)),
    (-20, (_c(_t('Exotic Plasma')) + _t('Baryon'), 0, 59737, 0, 40263)),
    (-21, (_c(_t('Exotic Plasma')) + _t('Tetryon'), 0, 69208, 0, 30792)),
    (-22, (_c(_t('Exotic Plasma')) + '|' + _t('[T2] Occult'), 0, 55863, 0, 44137)),
    # Different sizes of packs do different damage ratios, the values here
    # are average of ratios across sizes
    (-23, (_c(_t('Condenser Packs')) + '|' + _t('[T2] StrikeSnipe'), 51817, 0, 48183, 0)),
    (-24, (_c(_t('Condenser Packs')) + _t('MesmerFlux'), 76476, 0, 23524, 0)),
    (-25, (_c(_t('Condenser Packs')) + _t('SlamBolt'), 23376, 0, 76624, 0)),
    (-26, (_c(_t('Condenser Packs')) + _t('BlastShot'), 19820, 0, 80180, 0)),
    (-27, (_c(_t('Condenser Packs')) + _t('GalvaSurge'), 80206, 0, 19794, 0)),
    (-28, (_c(_t('Condenser Packs')) + '|' + _t('[T2] ElectroPunch'), 50547, 0, 49453, 0)),

    (-29, (_c(_t('Hybrid Charges')) + '|' + _t('[T2] Spike'), 0, 4, 4, 0)),
    (-30, (_c(_t('Hybrid Charges')) + '|' + _t('[T2] Null'), 0, 6, 5, 0)),
    (-31, (_c(_t('Hybrid Charges')) + _t('Iron'), 0, 2, 3, 0)),
    (-32, (_c(_t('Hybrid Charges')) + _t('Tungsten'), 0, 2, 4, 0)),
    (-33, (_c(_t('Hybrid Charges')) + _t('Iridium'), 0, 3, 4, 0)),
    (-34, (_c(_t('Hybrid Charges')) + _t('Lead'), 0, 3, 5, 0)),
    (-35, (_c(_t('Hybrid Charges')) + _t('Thorium'), 0, 4, 5, 0)),
    (-36, (_c(_t('Hybrid Charges')) + _t('Uranium'), 0, 4, 6, 0)),
    (-37, (_c(_t('Hybrid Charges')) + _t('Plutonium'), 0, 5, 6, 0)),
    (-38, (_c(_t('Hybrid Charges')) + _t('Antimatter'), 0, 5, 7, 0)),
    (-39, (_c(_t('Hybrid Charges')) + '|' + _t('[T2] Javelin'), 0, 8, 6, 0)),
    (-40, (_c(_t('Hybrid Charges')) + '|' + _t('[T2] Void'), 0, 7.7, 7.7, 0)),
    (-41, (_c(_t('Projectile Ammo')) + '|' + _t('[T2] Tremor'), 0, 0, 3, 5)),
    (-42, (_c(_t('Projectile Ammo')) + '|' + _t('[T2] Barrage'), 0, 0, 5, 6)),
    (-43, (_c(_t('Projectile Ammo')) + _t('Carbonized Lead'), 0, 0, 4, 1)),
    (-44, (_c(_t('Projectile Ammo')) + _t('Nuclear'), 0, 0, 1, 4)),
    (-45, (_c(_t('Projectile Ammo')) + _t('Proton'), 3, 0, 2, 0)),
    (-46, (_c(_t('Projectile Ammo')) + _t('Depleted Uranium'), 0, 3, 2, 3)),
    (-47, (_c(_t('Projectile Ammo')) + _t('Titanium Sabot'), 0, 0, 6, 2)),
    (-48, (_c(_t('Projectile Ammo')) + _t('EMP'), 9, 0, 1, 2)),
    (-49, (_c(_t('Projectile Ammo')) + _t('Phased Plasma'), 0, 10, 2, 0)),
    (-50, (_c(_t('Projectile Ammo')) + _t('Fusion'), 0, 0, 2, 10)),
    (-51, (_c(_t('Projectile Ammo')) + '|' + _t('[T2] Quake'), 0, 0, 5, 9)),
    (-52, (_c(_t('Projectile Ammo')) + '|' + _t('[T2] Hail'), 0, 0, 3.3, 12.1)),
    (-53, (_c(_t('Missiles')) + _t('Mjolnir'), 1, 0, 0, 0)),
    (-54, (_c(_t('Missiles')) + _t('Inferno'), 0, 1, 0, 0)),
    (-55, (_c(_t('Missiles')) + _t('Scourge'), 0, 0, 1, 0)),
    (-56, (_c(_t('Missiles')) + _t('Nova'), 0, 0, 0, 1)),
    (-57, (_c(_t('Bombs')) + _t('Electron Bomb'), 6400, 0, 0, 0)),
    (-58, (_c(_t('Bombs')) + _t('Scorch Bomb'), 0, 6400, 0, 0)),
    (-59, (_c(_t('Bombs')) + _t('Concussion Bomb'), 0, 0, 6400, 0)),
    (-60, (_c(_t('Bombs')) + _t('Shrapnel Bomb'), 0, 0, 0, 6400)),
    # Source: ticket #2067 and #2265
    (-61, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('All'), 126, 427, 218, 230)),
    (-62, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Angel'), 450, 72, 80, 398)),
    (-63, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Concord'), 53, 559, 94, 295)),
    (-64, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Drifter'), 250, 250, 250, 250)),
    (-65, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Drones'), 250, 250, 250, 250)),
    (-66, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Overmind'), 0, 410, 590, 0)),
    (-67, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Sansha'), 569, 431, 0, 0)),
    (-68, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Seeker'), 402, 402, 98, 98)),
    (-69, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Sleeper'), 313, 313, 187, 187)),
    (-70, (_c(_t('NPC')) + _c(_t('Abyssal')) + _t('Triglavian'), 0, 615, 0, 385)),
    (-71, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Angel Cartel'), 1838, 562, 2215, 3838)),
    (-72, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Blood Raiders'), 5067, 4214, 0, 0)),
    (-73, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Guristas'), 0, 1828, 7413, 0)),
    (-74, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Rogue Drone'), 394, 666, 1090, 1687)),
    (-75, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Sanshas Nation'), 5586, 4112, 0, 0)),
    (-76, (_c(_t('NPC')) + _c(_t('Asteroid')) + _t('Serpentis'), 0, 5373, 4813, 0)),
    (-77, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Enyo'), 0, 147, 147, 0)),
    (-78, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Hawk'), 0, 0, 247, 0)),
    (-79, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Jaguar'), 36, 0, 50, 182)),
    (-80, (_c(_t('NPC')) + _c(_t('Burner')) + _c(_t('Team')) + _t('Vengeance'), 232, 0, 0, 0)),
    (-81, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Cruor'), 90, 90, 0, 0)),
    (-82, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Dramiel'), 55, 0, 20, 96)),
    (-83, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Daredevil'), 0, 110, 154, 0)),
    (-84, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Succubus'), 135, 30, 0, 0)),
    (-85, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Worm'), 0, 0, 228, 0)),
    (-86, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Ashimmu'), 260, 100, 0, 0)),
    (-87, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Talos'), 0, 413, 413, 0)),
    (-88, (_c(_t('NPC')) + _c(_t('Burner')) + _t('Sentinel'), 0, 0, 75, 90)),
    (-89, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Angel Cartel'), 369, 533, 1395, 3302)),
    (-90, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Blood Raiders'), 6040, 5052, 10, 15)),
    (-91, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Guristas'), 0, 1531, 9680, 0)),
    (-92, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Rogue Drone'), 276, 1071, 1069, 871)),
    (-93, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Sanshas Nation'), 3009, 2237, 0, 0)),
    (-94, (_c(_t('NPC')) + _c(_t('Deadspace')) + _t('Serpentis'), 0, 3110, 1929, 0)),
    # Source: ticket #2067
    (-95, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Triglavian Entities')) + _t('Dread'), 0, 417, 0, 583)),
    (-96, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Triglavian Entities')) + _t('Normal Subcaps'), 0, 610, 0, 390)),
    # To avoid errors on msgfmt, we have to mark that '0%' is meaning literally 0% with no-python-format.
    # See also: https://github.com/vslavik/poedit/issues/645
    (-97, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Triglavian Entities')) +
           # xgettext:no-python-format
           _t('Subcaps w/missiles 0% spool up'), 367, 155, 367, 112)),
    (-98, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Triglavian Entities')) +
           # xgettext:no-python-format
           _t('Subcaps w/missiles 50% spool up'), 291, 243, 291, 175)),
    (-99, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Triglavian Entities')) +
           # xgettext:no-python-format
           _t('Subcaps w/missiles 100% spool up'), 241, 301, 241, 217)),
    (-100, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Amarr EDENCOM Entities')) + _t('Dread/Subcaps'), 583, 417, 0, 0)),
    (-101, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Caldari EDENCOM Entities')) + _t('Dread'), 1000, 0, 0, 0)),
    (-102, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Caldari EDENCOM Entities')) + _t('Subcaps'), 511, 21, 29, 440)),
    (-103, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Gallente EDENCOM Entities')) + _t('Dread/Subcaps'), 0, 417, 583, 0)),
    (-104, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Minmatar EDENCOM Entities')) + _t('Dread'), 0, 0, 583, 417)),
    (-105, (_c(_t('NPC')) + _c(_t('Invasion')) + _c(_t('Minmatar EDENCOM Entities')) + _t('Subcaps'), 302, 136, 328, 234)),
    (-106, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Drifter Entities'), 250, 250, 250, 250)),
    (-107, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Sleeper Entities'), 265, 265, 235, 235)),
    (-108, (_c(_t('NPC')) + _c(_t('Invasion')) + _t('Rogue Drone Entities'), 250, 250, 250, 250)),
    (-109, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Amarr Empire'), 4464, 3546, 97, 0)),
    (-110, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Caldari State'), 0, 2139, 4867, 0)),
    (-111, (_c(_t('NPC')) + _c(_t('Mission')) + _t('CONCORD'), 336, 134, 212, 412)),
    (-112, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Gallente Federation'), 9, 3712, 2758, 0)),
    (-113, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Khanid'), 612, 483, 43, 6)),
    (-114, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Minmatar Republic'), 1024, 388, 1655, 4285)),
    (-115, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Mordus Legion'), 25, 262, 625, 0)),
    (-116, (_c(_t('NPC')) + _c(_t('Mission')) + _t('Thukker'), 0, 52, 10, 79)),
    (-117, (_c(_t('NPC')) + _t('Sansha Incursion'), 1682, 1347, 3678, 3678)),
    (-118, (_c(_t('NPC')) + _t('Sleepers'), 1472, 1472, 1384, 1384))])


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

    def calculateEhp(self, item):
        ehp = {}
        for (type, attr) in (('shield', 'shieldCapacity'), ('armor', 'armorHP'), ('hull', 'hp')):
            rawCapacity = item.getModifiedItemAttr(attr)
            ehp[type] = self.effectivify(item, rawCapacity, type)

        return ehp

    def calculateEffectiveTank(self, fit, tankInfo):
        typeMap = {
            "passiveShield": "shield",
            "shieldRepair": "shield",
            "armorRepair": "armor",
            "armorRepairPreSpool": "armor",
            "armorRepairFullSpool": "armor",
            "hullRepair": "hull"
        }
        ereps = {}
        for field in tankInfo:
            if field in typeMap:
                ereps[field] = self.effectivify(fit.ship, tankInfo[field], typeMap[field])
        return ereps

    def effectivify(self, item, amount, type):
        type = type if type != "hull" else ""
        totalDamage = sum((self.emAmount, self.thermalAmount, self.kineticAmount, self.explosiveAmount))
        specificDivider = 0
        for damageType in self.DAMAGE_TYPES:
            # Compose an attribute name, then make sure the first letter is NOT capitalized
            attrName = "%s%sDamageResonance" % (type, damageType.capitalize())
            attrName = attrName[0].lower() + attrName[1:]

            resonance = item.getModifiedItemAttr(attrName)
            damage = getattr(self, "%sAmount" % damageType)

            specificDivider += damage / float(totalDamage or 1) * resonance

        return amount / (specificDivider or 1)

    importMap = {
        "em": "em",
        "therm": "thermal",
        "kin": "kinetic",
        "exp": "explosive"
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
