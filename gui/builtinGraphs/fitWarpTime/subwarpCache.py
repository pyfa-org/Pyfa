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
from gui.builtinGraphs.base import FitDataCache


class SubwarpSpeedCache(FitDataCache):

    def getSubwarpSpeed(self, fit):
        try:
            subwarpSpeed = self._data[fit.ID]
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
            for mod in fit.modules:
                if mod.item is not None and mod.item.group.name in disallowedGroups and mod.state >= FittingModuleState.ACTIVE:
                    modStates[mod] = mod.state
                    mod.state = FittingModuleState.ONLINE
            projFitStates = {}
            for projFit in fit.projectedFits:
                projectionInfo = projFit.getProjectionInfo(fit.ID)
                if projectionInfo is not None and projectionInfo.active:
                    projFitStates[projectionInfo] = projectionInfo.active
                    projectionInfo.active = False
            projModStates = {}
            for mod in fit.projectedModules:
                if not mod.isExclusiveSystemEffect and mod.state >= FittingModuleState.ACTIVE:
                    projModStates[mod] = mod.state
                    mod.state = FittingModuleState.ONLINE
            projDroneStates = {}
            for drone in fit.projectedDrones:
                if drone.amountActive > 0:
                    projDroneStates[drone] = drone.amountActive
                    drone.amountActive = 0
            projFighterStates = {}
            for fighter in fit.projectedFighters:
                if fighter.active:
                    projFighterStates[fighter] = fighter.active
                    fighter.active = False
            fit.calculateModifiedAttributes()
            subwarpSpeed = fit.ship.getModifiedItemAttr('maxVelocity')
            self._data[fit.ID] = subwarpSpeed
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
            fit.calculateModifiedAttributes()
        return subwarpSpeed
