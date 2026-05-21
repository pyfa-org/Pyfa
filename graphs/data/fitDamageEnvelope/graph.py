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

from graphs.data.base import FitGraph, Input, VectorDef, XDef, YDef
from service.settings import GraphSettings
from .getter import Distance2EnvelopeDpsGetter

_t = wx.GetTranslation


class FitDamageEnvelopeGraph(FitGraph):
    # UI stuff
    internalName = 'dmgEnvelopeGraph'
    name = _t('Damage Projection')
    xDefs = [XDef(handle='distance', unit='km', label=_t('Distance'), mainInput=('distance', 'km'))]
    inputs = [
        Input(handle='distance', unit='km', label=_t('Distance'), iconID=1391, defaultValue=None, defaultRange=(0, 100),
              mainTooltip=_t('Distance between the attacker and the target, as seen in overview (surface-to-surface)'),
              secondaryTooltip=_t(
                  'Distance between the attacker and the target, as seen in overview (surface-to-surface)')),
        Input(handle='tgtSpeed', unit='%', label=_t('Target speed'), iconID=1389, defaultValue=100,
              defaultRange=(0, 100)),
        Input(handle='tgtSigRad', unit='%', label=_t('Target signature'), iconID=1390, defaultValue=100,
              defaultRange=(100, 200), conditions=[(('tgtSigRad', 'm'), None), (('tgtSigRad', '%'), None)])]
    srcVectorDef = VectorDef(lengthHandle='atkSpeed', lengthUnit='%', angleHandle='atkAngle', angleUnit='degrees',
                             label=_t('Attacker'))
    tgtVectorDef = VectorDef(lengthHandle='tgtSpeed', lengthUnit='%', angleHandle='tgtAngle', angleUnit='degrees',
                             label=_t('Target'))
    hasTargets = True
    srcExtraCols = ('Dps', 'Speed', 'Radius')

    @property
    def yDefs(self):
        ignoreResists = GraphSettings.getInstance().get('ignoreResists')
        return [YDef(handle='dps', unit=None, label=_t('Best DPS') if ignoreResists else _t('Best effective DPS'))]

    @property
    def tgtExtraCols(self):
        cols = []
        if not GraphSettings.getInstance().get('ignoreResists'):
            cols.append('Target Resists')
        cols.extend(('Speed', 'SigRadius', 'Radius', 'FullHP'))
        return cols

    # Calculation stuff
    _normalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v * 1000,
        ('atkSpeed', '%'): lambda v, src, tgt: v / 100 * src.getMaxVelocity(),
        ('tgtSpeed', '%'): lambda v, src, tgt: v / 100 * tgt.getMaxVelocity(),
        ('tgtSigRad', '%'): lambda v, src, tgt: v / 100 * tgt.getSigRadius()}
    _getters = {('distance', 'dps'): Distance2EnvelopeDpsGetter}
    _denormalizers = {('distance', 'km'): lambda v, src, tgt: None if v is None else v / 1000,
        ('tgtSpeed', '%'): lambda v, src, tgt: v * 100 / tgt.getMaxVelocity(),
        ('tgtSigRad', '%'): lambda v, src, tgt: v * 100 / tgt.getSigRadius()}
