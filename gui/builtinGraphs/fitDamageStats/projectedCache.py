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


from gui.builtinGraphs.base import FitDataCache
from eos.const import FittingModuleState
from eos.modifiedAttributeDict import getResistanceAttrID


class ProjectedDataCache(FitDataCache):

    def getProjModData(self, fit):
        try:
            projectedData = self._data[fit.ID]['modules']
        except KeyError:
            # Format of items for both: (boost strength, optimal, falloff, stacking group, resistance attr ID)
            webMods = []
            tpMods = []
            projectedData = self._data.setdefault(fit.ID, {})['modules'] = (webMods, tpMods)
            for mod in fit.modules:
                if mod.state <= FittingModuleState.ONLINE:
                    continue
                for webEffectName in ('remoteWebifierFalloff', 'structureModuleEffectStasisWebifier'):
                    if webEffectName in mod.item.effects:
                        webMods.append((
                            mod.getModifiedItemAttr('speedFactor'),
                            mod.maxRange or 0,
                            mod.falloff or 0,
                            'default',
                            getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects[webEffectName])))
                if 'doomsdayAOEWeb' in mod.item.effects:
                    webMods.append((
                        mod.getModifiedItemAttr('speedFactor'),
                        max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange') - fit.ship.getModifiedItemAttr('radius')),
                        mod.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects['doomsdayAOEWeb'])))
                for tpEffectName in ('remoteTargetPaintFalloff', 'structureModuleEffectTargetPainter'):
                    if tpEffectName in mod.item.effects:
                        tpMods.append((
                            mod.getModifiedItemAttr('signatureRadiusBonus'),
                            mod.maxRange or 0,
                            mod.falloff or 0,
                            'default',
                            getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects[tpEffectName])))
                if 'doomsdayAOEPaint' in mod.item.effects:
                    tpMods.append((
                        mod.getModifiedItemAttr('signatureRadiusBonus'),
                        max(0, (mod.maxRange or 0) + mod.getModifiedItemAttr('doomsdayAOERange') - fit.ship.getModifiedItemAttr('radius')),
                        mod.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=mod, effect=mod.item.effects['doomsdayAOEPaint'])))
        return projectedData

    def getProjDroneData(self, fit):
        try:
            projectedData = self._data[fit.ID]['drones']
        except KeyError:
            # Format of items for both: (boost strength, optimal, falloff, stacking group, resistance attr ID, drone speed, drone radius)
            webDrones = []
            tpDrones = []
            projectedData = self._data.setdefault(fit.ID, {})['drones'] = (webDrones, tpDrones)
            for drone in fit.drones:
                if drone.amountActive <= 0:
                    continue
                if 'remoteWebifierEntity' in drone.item.effects:
                    webDrones.extend(drone.amountActive * ((
                        drone.getModifiedItemAttr('speedFactor'),
                        drone.maxRange or 0,
                        drone.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=drone, effect=drone.item.effects['remoteWebifierEntity']),
                        drone.getModifiedItemAttr('maxVelocity'),
                        drone.getModifiedItemAttr('radius')),))
                if 'remoteTargetPaintEntity' in drone.item.effects:
                    tpDrones.extend(drone.amountActive * ((
                        drone.getModifiedItemAttr('signatureRadiusBonus'),
                        drone.maxRange or 0,
                        drone.falloff or 0,
                        'default',
                        getResistanceAttrID(modifyingItem=drone, effect=drone.item.effects['remoteTargetPaintEntity']),
                        drone.getModifiedItemAttr('maxVelocity'),
                        drone.getModifiedItemAttr('radius')),))
        return projectedData

    def getProjFighterData(self, fit):
        try:
            projectedData = self._data[fit.ID]['fighters']
        except KeyError:
            # Format of items for both: (boost strength, optimal, falloff, stacking group, resistance attr ID, drone speed, drone radius)
            webFighters = []
            tpFighters = []
            projectedData = self._data.setdefault(fit.ID, {})['fighters'] = (webFighters, tpFighters)
            for fighter in fit.fighters:
                if not fighter.active:
                    continue
                for ability in fighter.abilities:
                    if not ability.active:
                        continue
                    if ability.effect.name == 'fighterAbilityStasisWebifier':
                        webFighters.extend((
                            fighter.getModifiedItemAttr('fighterAbilityStasisWebifierSpeedPenalty') * fighter.amountActive,
                            fighter.getModifiedItemAttr('fighterAbilityStasisWebifierOptimalRange'),
                            fighter.getModifiedItemAttr('fighterAbilityStasisWebifierFalloffRange'),
                            'default',
                            getResistanceAttrID(modifyingItem=fighter, effect=fighter.item.effects['fighterAbilityStasisWebifier']),
                            fighter.getModifiedItemAttr('maxVelocity'),
                            fighter.getModifiedItemAttr('radius')))
        return projectedData
