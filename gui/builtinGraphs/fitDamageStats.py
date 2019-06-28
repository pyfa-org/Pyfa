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


from .base import FitGraph, XDef, YDef, Input, VectorDef


class FitDamageStatsGraph(FitGraph):

    name = 'Damage Stats'

    # UI stuff
    @property
    def xDefs(self):
        return [
            XDef(handle='distance', unit='km', label='Distance', mainInput=('distance', 'km')),
            XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
            XDef(handle='tgtSpeed', unit='m/s', label='Target speed', mainInput=('tgtSpeed', '%')),
            XDef(handle='tgtSpeed', unit='%', label='Target speed', mainInput=('tgtSpeed', '%')),
            XDef(handle='tgtSigRad', unit='m', label='Target signature radius', mainInput=('tgtSigRad', '%')),
            XDef(handle='tgtSigRad', unit='%', label='Target signature radius', mainInput=('tgtSigRad', '%'))]

    @property
    def yDefs(self):
        return [
            YDef(handle='dps', unit=None, label='DPS'),
            YDef(handle='volley', unit=None, label='Volley'),
            YDef(handle='damage', unit=None, label='Damage inflicted')]

    @property
    def inputs(self):
        return [
            Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=None, defaultRange=(0, 80), mainOnly=False),
            Input(handle='distance', unit='km', label='Distance', iconID=1391, defaultValue=50, defaultRange=(0, 100), mainOnly=False),
            Input(handle='tgtSpeed', unit='%', label='Target speed', iconID=1389, defaultValue=100, defaultRange=(0, 100), mainOnly=False),
            Input(handle='tgtSigRad', unit='%', label='Target signature', iconID=1390, defaultValue=100, defaultRange=(100, 200), mainOnly=True)]

    @property
    def srcVectorDef(self):
        return VectorDef(lengthHandle='atkSpeed', lengthUnit='%', angleHandle='atkAngle', angleUnit='degrees', label='Attacker')

    @property
    def tgtVectorDef(self):
        return VectorDef(lengthHandle='tgtSpeed', lengthUnit='%', angleHandle='tgtAngle', angleUnit='degrees', label='Target')

    @property
    def hasTargets(self):
        return True

    # Calculation stuff
    _normalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v * 1000,
        ('atkSpeed', '%'): lambda v, fit, tgt: v * fit.ship.getModifiedItemAttr('maxVelocity', 0),
        ('tgtSpeed', '%'): lambda v, fit, tgt: v * tgt.ship.getModifiedItemAttr('maxVelocity', 0),
        ('tgtSigRad', '%'): lambda v, fit, tgt: v * fit.ship.getModifiedItemAttr('signatureRadius', 0)}

    _limiters = {
        'time': lambda fit, tgt: (0, 2500)}

    _denormalizers = {
        ('distance', 'km'): lambda v, fit, tgt: v / 1000,
        ('tgtSpeed', '%'): lambda v, fit, tgt: v / tgt.ship.getModifiedItemAttr('maxVelocity', 0),
        ('tgtSigRad', '%'): lambda v, fit, tgt: v / fit.ship.getModifiedItemAttr('signatureRadius', 0)}

    def _distance2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _distance2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _distance2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _time2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSpeed2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSpeed2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSpeed2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2dps(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2volley(self, mainInput, miscInputs, fit, tgt):
        return [], []

    def _tgtSigRad2damage(self, mainInput, miscInputs, fit, tgt):
        return [], []

    _getters = {
        ('distance', 'dps'): _distance2dps,
        ('distance', 'volley'): _distance2volley,
        ('distance', 'damage'): _distance2damage,
        ('time', 'dps'): _time2dps,
        ('time', 'volley'): _time2volley,
        ('time', 'damage'): _time2damage,
        ('tgtSpeed', 'dps'): _tgtSpeed2dps,
        ('tgtSpeed', 'volley'): _tgtSpeed2volley,
        ('tgtSpeed', 'damage'): _tgtSpeed2damage,
        ('tgtSigRad', 'dps'): _tgtSigRad2dps,
        ('tgtSigRad', 'volley'): _tgtSigRad2volley,
        ('tgtSigRad', 'damage'): _tgtSigRad2damage}


FitDamageStatsGraph.register()
