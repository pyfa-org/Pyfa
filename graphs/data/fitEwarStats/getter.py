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

from graphs.calc import calculateMultiplier, calculateRangeFactor
from graphs.data.base import SmoothPointGetter


class Distance2WebbingStrGetter(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        resonance = 1 - (miscParams['resist'] or 0)
        webs = []
        for mod in src.item.activeModulesIter():
            for effectName in ('remoteWebifierFalloff', 'structureModuleEffectStasisWebifier'):
                if effectName in mod.item.effects:
                    webs.append((
                        mod.getModifiedItemAttr('speedFactor') * resonance,
                        mod.maxRange or 0, mod.falloff or 0, 'default'))
            if 'doomsdayAOEWeb' in mod.item.effects:
                webs.append((
                    mod.getModifiedItemAttr('speedFactor') * resonance,
                    max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange') - src.getRadius()),
                    mod.falloff or 0, 'default'))
        for drone in src.item.activeDronesIter():
            if 'remoteWebifierEntity' in drone.item.effects:
                webs.extend(drone.amountActive * ((
                    drone.getModifiedItemAttr('speedFactor') * resonance,
                    src.item.extraAttributes['droneControlRange'], 0, 'default'),))
        for fighter, ability in src.item.activeFighterAbilityIter():
            if ability.effect.name == 'fighterAbilityStasisWebifier':
                webs.append((
                    fighter.getModifiedItemAttr('fighterAbilityStasisWebifierSpeedPenalty') * fighter.amountActive * resonance,
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


class Distance2DampStrLockRangeGetter(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        resonance = 1 - (miscParams['resist'] or 0)
        damps = []
        for mod in src.item.activeModulesIter():
            for effectName in ('remoteSensorDampFalloff', 'structureModuleEffectRemoteSensorDampener'):
                if effectName in mod.item.effects:
                    damps.append((
                        mod.getModifiedItemAttr('maxTargetRangeBonus') * resonance,
                        mod.maxRange or 0, mod.falloff or 0, 'default'))
            if 'doomsdayAOEDamp' in mod.item.effects:
                damps.append((
                    mod.getModifiedItemAttr('maxTargetRangeBonus') * resonance,
                    max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange') - src.getRadius()),
                    mod.falloff or 0, 'default'))
        for drone in src.item.activeDronesIter():
            if 'remoteSensorDampEntity' in drone.item.effects:
                damps.extend(drone.amountActive * ((
                    drone.getModifiedItemAttr('maxTargetRangeBonus') * resonance,
                    src.item.extraAttributes['droneControlRange'], 0, 'default'),))
        return {'damps': damps}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        distance = x
        strMults = {}
        for strength, optimal, falloff, stackingGroup in commonData['damps']:
            strength *= calculateRangeFactor(srcOptimalRange=optimal, srcFalloffRange=falloff, distance=distance)
            strMults.setdefault(stackingGroup, []).append((1 + strength / 100, None))
        strMult = calculateMultiplier(strMults)
        strength = (1 - strMult) * 100
        return strength


class Distance2TdStrOptimalGetter(SmoothPointGetter):

    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        resonance = 1 - (miscParams['resist'] or 0)
        tds = []
        for mod in src.item.activeModulesIter():
            for effectName in ('shipModuleTrackingDisruptor', 'structureModuleEffectWeaponDisruption'):
                if effectName in mod.item.effects:
                    tds.append((
                        mod.getModifiedItemAttr('maxRangeBonus') * resonance,
                        mod.maxRange or 0, mod.falloff or 0, 'default'))
            if 'doomsdayAOETrack' in mod.item.effects:
                tds.append((
                    mod.getModifiedItemAttr('maxRangeBonus') * resonance,
                    max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange') - src.getRadius()),
                    mod.falloff or 0, 'default'))
        for drone in src.item.activeDronesIter():
            if 'npcEntityWeaponDisruptor' in drone.item.effects:
                tds.extend(drone.amountActive * ((
                    drone.getModifiedItemAttr('maxRangeBonus') * resonance,
                    src.item.extraAttributes['droneControlRange'], 0, 'default'),))
        return {'tds': tds}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        distance = x
        strMults = {}
        for strength, optimal, falloff, stackingGroup in commonData['tds']:
            strength *= calculateRangeFactor(srcOptimalRange=optimal, srcFalloffRange=falloff, distance=distance)
            strMults.setdefault(stackingGroup, []).append((1 + strength / 100, None))
        strMult = calculateMultiplier(strMults)
        strength = (1 - strMult) * 100
        return strength
