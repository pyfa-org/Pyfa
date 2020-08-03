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


import wx

from graphs.data.base import FitGraph, Input, InputCheckbox, XDef, YDef
from .getter import CapAmount2CapAmountGetter, CapAmount2CapRegenGetter, Time2CapAmountGetter, Time2CapRegenGetter

_t = wx.GetTranslation


class FitCapacitorGraph(FitGraph):
    # UI stuff
    internalName = 'capacitorGraph'
    name = _t('Capacitor')
    xDefs = [
        XDef(handle='time', unit='s', label=_t('Time'), mainInput=('time', 's')),
        XDef(handle='capAmount', unit='GJ', label=_t('Cap amount'), mainInput=('capAmount', '%')),
        XDef(handle='capAmount', unit='%', label=_t('Cap amount'), mainInput=('capAmount', '%'))]
    yDefs = [
        YDef(handle='capAmount', unit='GJ', label=_t('Cap amount')),
        YDef(handle='capRegen', unit='GJ/s', label=_t('Cap regen'))]
    inputs = [
        Input(handle='time', unit='s', label=_t('Time'), iconID=1392, defaultValue=120, defaultRange=(0, 300), conditions=[
            (('time', 's'), None)]),
        Input(handle='capAmount', unit='%', label=_t('Cap amount'), iconID=1668, defaultValue=25, defaultRange=(0, 100), conditions=[
            (('capAmount', 'GJ'), None),
            (('capAmount', '%'), None)]),
        Input(handle='capAmountT0', unit='%', label=_t('Starting cap amount'), iconID=1668, defaultValue=100, defaultRange=(0, 100), conditions=[
            (('time', 's'), None)])]
    checkboxes = [InputCheckbox(handle='useCapsim', label=_t('Use capacitor simulator'), defaultValue=True, conditions=[
        (('time', 's'), ('capAmount', 'GJ'))])]
    srcExtraCols = ('CapAmount', 'CapTime')

    # Calculation stuff
    _normalizers = {
        ('capAmount', '%'): lambda v, src, tgt: v / 100 * src.item.ship.getModifiedItemAttr('capacitorCapacity'),
        ('capAmountT0', '%'): lambda v, src, tgt: None if v is None else v / 100 * src.item.ship.getModifiedItemAttr('capacitorCapacity')}
    _limiters = {
        'time': lambda src, tgt: (0, 3600),
        'capAmount': lambda src, tgt: (0, src.item.ship.getModifiedItemAttr('capacitorCapacity')),
        'capAmountT0': lambda src, tgt: (0, src.item.ship.getModifiedItemAttr('capacitorCapacity'))}
    _getters = {
        ('time', 'capAmount'): Time2CapAmountGetter,
        ('time', 'capRegen'): Time2CapRegenGetter,
        ('capAmount', 'capAmount'): CapAmount2CapAmountGetter,
        ('capAmount', 'capRegen'): CapAmount2CapRegenGetter}
    _denormalizers = {('capAmount', '%'): lambda v, src, tgt: v * 100 / src.item.ship.getModifiedItemAttr('capacitorCapacity')}
