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


from gui.builtinGraphs.base import FitGraph, XDef, YDef, Input
from .getter import (
    Time2ShieldAmountGetter, Time2ShieldRegenGetter,
    ShieldAmount2ShieldAmountGetter, ShieldAmount2ShieldRegenGetter)


class FitShieldRegenGraph(FitGraph):

    # UI stuff
    internalName = 'shieldRegenGraph'
    name = 'Shield Regeneration'
    xDefs = [
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
        XDef(handle='shieldAmount', unit='EHP', label='Shield amount', mainInput=('shieldAmount', '%')),
        XDef(handle='shieldAmount', unit='HP', label='Shield amount', mainInput=('shieldAmount', '%')),
        XDef(handle='shieldAmount', unit='%', label='Shield amount', mainInput=('shieldAmount', '%'))]
    yDefs = [
        YDef(handle='shieldAmount', unit='EHP', label='Shield amount'),
        YDef(handle='shieldAmount', unit='HP', label='Shield amount'),
        YDef(handle='shieldRegen', unit='EHP/s', label='Shield regen'),
        YDef(handle='shieldRegen', unit='HP/s', label='Shield regen')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=120, defaultRange=(0, 300), mainOnly=True),
        Input(handle='shieldAmount', unit='%', label='Shield amount', iconID=1384, defaultValue=25, defaultRange=(0, 100), mainOnly=True)]
    srcExtraCols = ('ShieldAmount', 'ShieldTime')

    # Calculation stuff
    _normalizers = {
        ('shieldAmount', '%'): lambda v, fit, tgt: v / 100 * fit.ship.getModifiedItemAttr('shieldCapacity')}
    _limiters = {
        'shieldAmount': lambda fit, tgt: (0, fit.ship.getModifiedItemAttr('shieldCapacity'))}
    _denormalizers = {
        ('shieldAmount', '%'): lambda v, fit, tgt: v * 100 / fit.ship.getModifiedItemAttr('shieldCapacity'),
        ('shieldAmount', 'EHP'): lambda v, fit, tgt: fit.damagePattern.effectivify(fit, v, 'shield'),
        ('shieldRegen', 'EHP/s'): lambda v, fit, tgt: fit.damagePattern.effectivify(fit, v, 'shield')}
    _getters = {
        ('time', 'shieldAmount'): Time2ShieldAmountGetter,
        ('time', 'shieldRegen'): Time2ShieldRegenGetter,
        ('shieldAmount', 'shieldAmount'): ShieldAmount2ShieldAmountGetter,
        ('shieldAmount', 'shieldRegen'): ShieldAmount2ShieldRegenGetter}


FitShieldRegenGraph.register()
