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

import gui.mainFrame
from graphs.data.base import FitGraph, Input, XDef, YDef
from .getter import (ShieldAmount2ShieldAmountGetter, ShieldAmount2ShieldRegenGetter, Time2ShieldAmountGetter, Time2ShieldRegenGetter)

_t = wx.GetTranslation


class FitShieldRegenGraph(FitGraph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.isEffective = gui.mainFrame.MainFrame.getInstance().statsPane.nameViewMap['resistancesViewFull'].showEffective

    # UI stuff
    internalName = 'shieldRegenGraph'
    name = _t('Shield Regeneration')
    inputs = [
        Input(handle='time', unit='s', label=_t('Time'), iconID=1392, defaultValue=120, defaultRange=(0, 300), conditions=[
            (('time', 's'), None)]),
        Input(handle='shieldAmount', unit='%', label=_t('Shield amount'), iconID=1384, defaultValue=25, defaultRange=(0, 100), conditions=[
            (('shieldAmount', 'EHP'), None),
            (('shieldAmount', 'HP'), None),
            (('shieldAmount', '%'), None)]),
        Input(handle='shieldAmountT0', unit='%', label=_t('Starting shield amount'), iconID=1384, defaultValue=0, defaultRange=(0, 100), conditions=[
            (('time', 's'), None)])]
    srcExtraCols = ('ShieldAmount', 'ShieldTime')
    usesHpEffectivity = True

    @property
    def xDefs(self):
        return [
            XDef(handle='time', unit='s', label=_t('Time'), mainInput=('time', 's')),
            XDef(handle='shieldAmount', unit='EHP' if self.isEffective else 'HP', label=_t('Shield amount'), mainInput=('shieldAmount', '%')),
            XDef(handle='shieldAmount', unit='%', label=_t('Shield amount'), mainInput=('shieldAmount', '%'))]

    @property
    def yDefs(self):
        return [
            YDef(handle='shieldAmount', unit='EHP' if self.isEffective else 'HP', label=_t('Shield amount')),
            YDef(handle='shieldRegen', unit='EHP/s' if self.isEffective else 'HP/s', label=_t('Shield regen'))]

    # Calculation stuff
    _normalizers = {
        ('shieldAmount', '%'): lambda v, src, tgt: v / 100 * src.item.ship.getModifiedItemAttr('shieldCapacity'),
        ('shieldAmountT0', '%'): lambda v, src, tgt: None if v is None else v / 100 * src.item.ship.getModifiedItemAttr('shieldCapacity'),
        # Needed only for "x mark" support, to convert EHP x into normalized value
        ('shieldAmount', 'EHP'): lambda v, src, tgt: v / src.item.damagePattern.effectivify(src.item.ship, 1, 'shield')}
    _limiters = {
        'shieldAmount': lambda src, tgt: (0, src.item.ship.getModifiedItemAttr('shieldCapacity')),
        'shieldAmountT0': lambda src, tgt: (0, src.item.ship.getModifiedItemAttr('shieldCapacity'))}
    _getters = {
        ('time', 'shieldAmount'): Time2ShieldAmountGetter,
        ('time', 'shieldRegen'): Time2ShieldRegenGetter,
        ('shieldAmount', 'shieldAmount'): ShieldAmount2ShieldAmountGetter,
        ('shieldAmount', 'shieldRegen'): ShieldAmount2ShieldRegenGetter}
    _denormalizers = {
        ('shieldAmount', '%'): lambda v, src, tgt: v * 100 / src.item.ship.getModifiedItemAttr('shieldCapacity'),
        ('shieldAmount', 'EHP'): lambda v, src, tgt: src.item.damagePattern.effectivify(src.item.ship, v, 'shield'),
        ('shieldRegen', 'EHP/s'): lambda v, src, tgt: src.item.damagePattern.effectivify(src.item.ship, v, 'shield')}
