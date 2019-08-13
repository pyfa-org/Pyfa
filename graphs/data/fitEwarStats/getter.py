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

from eos.const import FittingModuleState
from graphs.calc import calculateMultiplier, calculateRangeFactor
from graphs.data.base import SmoothPointGetter


class Distance2WebbingStrengthGetter(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        resist = dict(miscParams)['resist'] or 0
        webs = []
        for mod in src.item.modules:
            if mod.state <= FittingModuleState.ONLINE:
                continue
            for webEffectName in ('remoteWebifierFalloff', 'structureModuleEffectStasisWebifier'):
                if webEffectName in mod.item.effects:
                    webs.append((
                        mod.getModifiedItemAttr('speedFactor') * (1 - resist),
                        mod.maxRange or 0, mod.falloff or 0, 'default'))
            if 'doomsdayAOEWeb' in mod.item.effects:
                webs.append((
                    mod.getModifiedItemAttr('speedFactor') * (1 - resist),
                    max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange') - src.getRadius()),
                    mod.falloff or 0, 'default'))
        for drone in src.item.drones:
            if drone.amountActive <= 0:
                continue
            if 'remoteWebifierEntity' in drone.item.effects:
                webs.extend(drone.amountActive * ((
                    drone.getModifiedItemAttr('speedFactor') * (1 - resist),
                    src.item.extraAttributes['droneControlRange'], 0, 'default'),))
        for fighter in src.item.fighters:
            if not fighter.active:
                continue
            for ability in fighter.abilities:
                if not ability.active:
                    continue
                if ability.effect.name == 'fighterAbilityStasisWebifier':
                    webs.append((
                        fighter.getModifiedItemAttr('fighterAbilityStasisWebifierSpeedPenalty') * fighter.amountActive * (1 - resist),
                        math.inf, 0, 'default'))
        return {'webs': webs}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        distance = x
        strMults = {}
        for strength, optimal, falloff, stackingGroup in commonData['webs']:
            strength *= calculateRangeFactor(srcOptimalRange=optimal, srcFalloffRange=falloff, distance=distance)
            strMults.setdefault(stackingGroup, []).append((1 + strength / 100, None))
        strMult = calculateMultiplier(strMults)
        strength = (1 - strMult) * 100
        return strength
