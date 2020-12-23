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


from collections import namedtuple

from eos.modifiedAttributeDict import getResistanceAttrID
from graphs.data.base import FitDataCache


ModProjData = namedtuple('ModProjData', ('boost', 'optimal', 'falloff', 'stackingGroup', 'resAttrID'))
MobileProjData = namedtuple('MobileProjData', ('boost', 'optimal', 'falloff', 'stackingGroup', 'resAttrID', 'speed', 'radius'))


class ProjectedDataCache(FitDataCache):

    def getProjModData(self, src):
        try:
            projectedData = self._data[src.item.ID]['modules']
        except KeyError:
            # Format of items for both: (boost strength, optimal, falloff, stacking group, resistance attr ID)
            webMods = []
            tpMods = []
            projectedData = self._data.setdefault(src.item.ID, {})['modules'] = (webMods, tpMods)
            for mod in src.item.activeModulesIter():
                for webEffectName in ('remoteWebifierFalloff', 'structureModuleEffectStasisWebifier'):
                    if webEffectName in mod.item.effects:
                        webMods.append(ModProjData(
                            mod.getModifiedItemAttr('speedFactor'),
                            mod.maxRange or 0,
                            mod.falloff or 0,
                            'default',
                            getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects[webEffectName])))
                if 'doomsdayAOEWeb' in mod.item.effects:
                    webMods.append(ModProjData(
                        mod.getModifiedItemAttr('speedFactor'),
                        max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange')),
                        mod.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects['doomsdayAOEWeb'])))
                for tpEffectName in ('remoteTargetPaintFalloff', 'structureModuleEffectTargetPainter'):
                    if tpEffectName in mod.item.effects:
                        tpMods.append(ModProjData(
                            mod.getModifiedItemAttr('signatureRadiusBonus'),
                            mod.maxRange or 0,
                            mod.falloff or 0,
                            'default',
                            getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects[tpEffectName])))
                if 'doomsdayAOEPaint' in mod.item.effects:
                    tpMods.append(ModProjData(
                        mod.getModifiedItemAttr('signatureRadiusBonus'),
                        max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange')),
                        mod.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects['doomsdayAOEPaint'])))
        return projectedData

    def getProjDroneData(self, src):
        try:
            projectedData = self._data[src.item.ID]['drones']
        except KeyError:
            # Format of items for both: (boost strength, optimal, falloff, stacking group, resistance attr ID, drone speed, drone radius)
            webDrones = []
            tpDrones = []
            projectedData = self._data.setdefault(src.item.ID, {})['drones'] = (webDrones, tpDrones)
            for drone in src.item.activeDronesIter():
                if 'remoteWebifierEntity' in drone.item.effects:
                    webDrones.extend(drone.amountActive * (MobileProjData(
                        drone.getModifiedItemAttr('speedFactor'),
                        drone.maxRange or 0,
                        drone.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=drone, effect=drone.item.effects['remoteWebifierEntity']),
                        drone.getModifiedItemAttr('maxVelocity'),
                        drone.getModifiedItemAttr('radius')),))
                if 'remoteTargetPaintEntity' in drone.item.effects:
                    tpDrones.extend(drone.amountActive * (MobileProjData(
                        drone.getModifiedItemAttr('signatureRadiusBonus'),
                        drone.maxRange or 0,
                        drone.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=drone, effect=drone.item.effects['remoteTargetPaintEntity']),
                        drone.getModifiedItemAttr('maxVelocity'),
                        drone.getModifiedItemAttr('radius')),))
        return projectedData

    def getProjFighterData(self, src):
        try:
            projectedData = self._data[src.item.ID]['fighters']
        except KeyError:
            # Format of items for both: (boost strength, optimal, falloff, stacking group, resistance attr ID, fighter speed, fighter radius)
            webFighters = []
            tpFighters = []
            projectedData = self._data.setdefault(src.item.ID, {})['fighters'] = (webFighters, tpFighters)
            for fighter, ability in src.item.activeFighterAbilityIter():
                if ability.effect.name == 'fighterAbilityStasisWebifier':
                    webFighters.append(MobileProjData(
                        fighter.getModifiedItemAttr('fighterAbilityStasisWebifierSpeedPenalty') * fighter.amount,
                        fighter.getModifiedItemAttr('fighterAbilityStasisWebifierOptimalRange'),
                        fighter.getModifiedItemAttr('fighterAbilityStasisWebifierFalloffRange'),
                        'default',
                        getResistanceAttrID(modifyingItem=fighter, effect=fighter.item.effects['fighterAbilityStasisWebifier']),
                        fighter.getModifiedItemAttr('maxVelocity'),
                        fighter.getModifiedItemAttr('radius')))
        return projectedData
