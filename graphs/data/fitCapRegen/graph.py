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


from graphs.data.base import FitGraph, Input, XDef, YDef
from .getter import CapAmount2CapAmountGetter, CapAmount2CapRegenGetter, Time2CapAmountGetter, Time2CapRegenGetter


class FitCapRegenGraph(FitGraph):

    # UI stuff
    internalName = 'capRegenGraph'
    name = 'Capacitor Regeneration'
    xDefs = [
        XDef(handle='time', unit='s', label='Time', mainInput=('time', 's')),
        XDef(handle='capAmount', unit='GJ', label='Cap amount', mainInput=('capAmount', '%')),
        XDef(handle='capAmount', unit='%', label='Cap amount', mainInput=('capAmount', '%'))]
    yDefs = [
        YDef(handle='capAmount', unit='GJ', label='Cap amount'),
        YDef(handle='capRegen', unit='GJ/s', label='Cap regen')]
    inputs = [
        Input(handle='time', unit='s', label='Time', iconID=1392, defaultValue=120, defaultRange=(0, 300), mainOnly=True),
        Input(handle='capAmount', unit='%', label='Cap amount', iconID=1668, defaultValue=25, defaultRange=(0, 100), mainOnly=True)]
    srcExtraCols = ('CapAmount', 'CapTime')

    # Calculation stuff
    _normalizers = {
        ('capAmount', '%'): lambda v, src, tgt: v / 100 * src.item.ship.getModifiedItemAttr('capacitorCapacity')}
    _limiters = {
        'capAmount': lambda src, tgt: (0, src.item.ship.getModifiedItemAttr('capacitorCapacity'))}
    _getters = {
        ('time', 'capAmount'): Time2CapAmountGetter,
        ('time', 'capRegen'): Time2CapRegenGetter,
        ('capAmount', 'capAmount'): CapAmount2CapAmountGetter,
        ('capAmount', 'capRegen'): CapAmount2CapRegenGetter}
    _denormalizers = {
        ('capAmount', '%'): lambda v, src, tgt: v * 100 / src.item.ship.getModifiedItemAttr('capacitorCapacity')}
