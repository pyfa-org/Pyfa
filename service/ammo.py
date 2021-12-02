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


import math
from collections import OrderedDict

import wx

from eos.const import FittingHardpoint
from eos.saveddata.module import Module
from eos.utils.stats import DmgTypes
from service.market import Market


_t = wx.GetTranslation


class Ammo:

    instance = None

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Ammo()

        return cls.instance

    @staticmethod
    def getModuleFlatAmmo(mod):
        sMkt = Market.getInstance()
        if mod is None or mod.isEmpty:
            return set()
        chargeSet = set()
        # Do not try to grab it for t3d modes which can also be passed as part of selection
        if isinstance(mod, Module):
            for charge in mod.getValidCharges():
                if sMkt.getPublicityByItem(charge):
                    chargeSet.add(charge)
        return chargeSet

    @classmethod
    def getModuleStructuredAmmo(cls, mod, ammo=None):
        chargesFlat = cls.getModuleFlatAmmo(mod) if ammo is None else ammo
        # Make sure we do not consider mining turrets as combat turrets
        if mod.hardpoint == FittingHardpoint.TURRET and not mod.getModifiedItemAttr('miningAmount'):

            def turretSorter(charge):
                damage = 0
                range_ = (mod.item.getAttribute('maxRange')) * \
                         (charge.getAttribute('weaponRangeMultiplier') or 1)
                falloff = (mod.item.getAttribute('falloff') or 0) * \
                          (charge.getAttribute('fallofMultiplier') or 1)
                for type_ in DmgTypes.names():
                    d = charge.getAttribute('%sDamage' % type_)
                    if d > 0:
                        damage += d
                # Take optimal and falloff as range factor
                rangeFactor = range_ + falloff
                return -rangeFactor, charge.typeName.rsplit()[-2:], damage, charge.name

            all = OrderedDict()
            sub = []
            prevNameBase = None
            prevRange = None
            for charge in sorted(chargesFlat, key=turretSorter):
                if 'civilian' in charge.typeName.lower():
                    continue
                currNameBase = ' '.join(charge.typeName.rsplit()[-2:])
                currRange = charge.getAttribute('weaponRangeMultiplier')
                if sub and (currRange != prevRange or currNameBase != prevNameBase):
                    all[sub[0].name] = sub
                    sub = []
                sub.append(charge)
                prevNameBase = currNameBase
                prevRange = currRange
            else:
                if sub:
                    all[sub[0].name] = sub
            return 'ddTurret', all

        elif mod.hardpoint == FittingHardpoint.MISSILE and mod.item.name != 'Festival Launcher':

            def getChargeDamageInfo(charge):
                # Set up data storage for missile damage stuff
                damageMap = {}
                totalDamage = 0
                # Fill them with the data about charge
                for damageType in DmgTypes.names():
                    currentDamage = charge.getAttribute('{}Damage'.format(damageType)) or 0
                    damageMap[damageType] = currentDamage
                    totalDamage += currentDamage
                # Detect type of ammo
                chargeDamageType = None
                for damageType in damageMap:
                    # If all damage belongs to certain type purely, set appropriate
                    # ammoType
                    if damageMap[damageType] == totalDamage:
                        chargeDamageType = damageType
                        break
                # Else consider ammo as mixed damage
                if chargeDamageType is None:
                    chargeDamageType = 'mixed'
                return chargeDamageType, totalDamage

            def missileSorter(charge):
                # Get charge damage type and total damage
                chargeDamageType, totalDamage = getChargeDamageInfo(charge)
                # Find its position in sort list
                try:
                    position = DmgTypes.names().index(chargeDamageType)
                # Put charges which have non-standard damage type after charges with
                # standard damage type
                except ValueError:
                    position = math.inf
                return position, totalDamage, charge.name

            all = OrderedDict()
            sub = []
            prevType = None
            for charge in sorted(chargesFlat, key=missileSorter):
                currType = getChargeDamageInfo(charge)[0]
                if sub and currType != prevType:
                    all[prevType] = sub
                    sub = []
                sub.append(charge)
                prevType = currType
            else:
                if sub:
                    all[prevType] = sub
            return 'ddMissile', all

        elif mod.item.group.name == 'Frequency Mining Laser':

            def crystalSorter(charge):
                if charge.name.endswith(' II'):
                    techLvl = 2
                elif charge.name.endswith(' I'):
                    techLvl = 1
                else:
                    techLvl = 0
                if ' A ' in charge.name:
                    type_ = 'A'
                elif ' B ' in charge.name:
                    type_ = 'B'
                elif ' C ' in charge.name:
                    type_ = 'C'
                else:
                    type_ = '0'
                return type_, techLvl, charge.name

            typeMap = {
                253: 'a1',
                254: 'a2',
                255: 'a3',
                256: 'a4',
                257: 'a5',
                258: 'a6',
                259: 'r4',
                260: 'r8',
                261: 'r16',
                262: 'r32',
                263: 'r64'}

            prelim = {}
            for charge in chargesFlat:
                oreTypeList = charge.getAttribute('specializationAsteroidTypeList')
                category = typeMap.get(oreTypeList, _t('Misc'))
                prelim.setdefault(category, set()).add(charge)

            final = OrderedDict()
            for category, charges in prelim.items():
                final[category] = sorted(charges, key=crystalSorter)

            return 'miner', final

        else:

            def nameSorter(charge):
                parts = charge.name.split(" ")
                return [int(p) if p.isdigit() else p for p in parts]

            return 'general', {'general': sorted(chargesFlat, key=nameSorter)}
