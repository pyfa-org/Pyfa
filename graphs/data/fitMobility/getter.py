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

from graphs.data.base import SmoothPointGetter


class Time2DistanceGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxSpeed': src.getMaxVelocity(),
            'mass': src.item.ship.getModifiedItemAttr('mass'),
            'agility': src.item.ship.getModifiedItemAttr('agility')}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        time = x
        maxSpeed = commonData['maxSpeed']
        mass = commonData['mass']
        agility = commonData['agility']
        # Definite integral of:
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        distance_t = maxSpeed * time + (maxSpeed * agility * mass * math.exp((-time * 1000000) / (agility * mass)) / 1000000)
        distance_0 = maxSpeed * 0 + (maxSpeed * agility * mass * math.exp((-0 * 1000000) / (agility * mass)) / 1000000)
        distance = distance_t - distance_0
        return distance


class Time2SpeedGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        return {
            'maxSpeed': src.getMaxVelocity(),
            'mass': src.item.ship.getModifiedItemAttr('mass'),
            'agility': src.item.ship.getModifiedItemAttr('agility')}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        time = x
        maxSpeed = commonData['maxSpeed']
        mass = commonData['mass']
        agility = commonData['agility']
        # https://wiki.eveuniversity.org/Acceleration#Mathematics_and_formulae
        speed = maxSpeed * (1 - math.exp((-time * 1000000) / (agility * mass)))
        return speed


class Time2MomentumGetter(Time2SpeedGetter):

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        mass = commonData['mass']
        speed = Time2SpeedGetter._calculatePoint(
            self, x=x, miscParams=miscParams,
            src=src, tgt=tgt, commonData=commonData)
        momentum = speed * mass
        return momentum


class Time2BumpSpeedGetter(Time2SpeedGetter):

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        # S. Santorine, Ship Motion in EVE-Online, p3, Collisions & Bumping section
        # https://docs.google.com/document/d/1rwVWjTvzVdPEFETf0vwm649AFb4bgRBaNLpRPaoB03o
        # Internally, Santorine's formulas are using millions of kilograms, so we normalize to them here
        bumperMass = commonData['mass'] / 10 ** 6
        bumperSpeed = Time2SpeedGetter._calculatePoint(
            self, x=x, miscParams=miscParams,
            src=src, tgt=tgt, commonData=commonData)
        tgtMass = miscParams['tgtMass'] / 10 ** 6
        tgtSpeed = (2 * bumperSpeed * bumperMass) / (bumperMass + tgtMass)
        return tgtSpeed


class Time2BumpDistanceGetter(Time2BumpSpeedGetter):

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        # S. Santorine, Ship Motion in EVE-Online, p3, Collisions & Bumping section
        # https://docs.google.com/document/d/1rwVWjTvzVdPEFETf0vwm649AFb4bgRBaNLpRPaoB03o
        # Internally, Santorine's formulas are using millions of kilograms, so we normalize to them here
        tgtMass = miscParams['tgtMass'] / 10 ** 6
        tgtInertia = miscParams['tgtInertia']
        tgtSpeed = Time2BumpSpeedGetter._calculatePoint(
            self, x=x, miscParams=miscParams,
            src=src, tgt=tgt, commonData=commonData)
        tgtDistance = tgtSpeed * tgtMass * tgtInertia
        return tgtDistance
