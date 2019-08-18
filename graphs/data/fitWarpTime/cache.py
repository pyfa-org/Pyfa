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


from eos.const import FittingModuleState
from graphs.data.base import FitDataCache


class SubwarpSpeedCache(FitDataCache):

    def getSubwarpSpeed(self, src):
        try:
            subwarpSpeed = self._data[src.item.ID]
        except KeyError:
            modStates = {}
            disallowedGroups = (
                # Active modules which affect ship speed and cannot be used in warp
                'Propulsion Module',
                'Mass Entanglers',
                'Cloaking Device',
                # Those reduce ship speed to 0
                'Siege Module',
                'Super Weapon',
                'Cynosural Field Generator',
                'Clone Vat Bay',
                'Jump Portal Generator')
            for mod in src.item.activeModulesIter():
                if mod.item is not None and mod.item.group.name in disallowedGroups:
                    modStates[mod] = mod.state
                    mod.state = FittingModuleState.ONLINE
            projFitStates = {}
            for projFit in src.item.projectedFits:
                projectionInfo = projFit.getProjectionInfo(src.item.ID)
                if projectionInfo is not None and projectionInfo.active:
                    projFitStates[projectionInfo] = projectionInfo.active
                    projectionInfo.active = False
            projModStates = {}
            for mod in src.item.projectedModules:
                if not mod.isExclusiveSystemEffect and mod.state >= FittingModuleState.ACTIVE:
                    projModStates[mod] = mod.state
                    mod.state = FittingModuleState.ONLINE
            projDroneStates = {}
            for drone in src.item.projectedDrones:
                if drone.amountActive > 0:
                    projDroneStates[drone] = drone.amountActive
                    drone.amountActive = 0
            projFighterStates = {}
            for fighter in src.item.projectedFighters:
                if fighter.active:
                    projFighterStates[fighter] = fighter.active
                    fighter.active = False
            src.item.calculateModifiedAttributes()
            subwarpSpeed = src.getMaxVelocity()
            self._data[src.item.ID] = subwarpSpeed
            for projInfo, state in projFitStates.items():
                projInfo.active = state
            for mod, state in modStates.items():
                mod.state = state
            for mod, state in projModStates.items():
                mod.state = state
            for drone, amountActive in projDroneStates.items():
                drone.amountActive = amountActive
            for fighter, state in projFighterStates.items():
                fighter.active = state
            src.item.calculateModifiedAttributes()
        return subwarpSpeed
