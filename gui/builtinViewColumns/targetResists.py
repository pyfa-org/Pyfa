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

# noinspection PyPackageRequirements
import wx

from graphs.wrapper import TargetWrapper
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn
from service.const import TargetResistMode


class TargetResists(ViewColumn):

    name = 'Target Resists'
    proportionWidth = 5

    def __init__(self, fittingView, params):
        super().__init__(fittingView)
        self.imageId = fittingView.imageList.GetImageIndex(1393, 'icons')
        self.bitmap = BitmapLoader.getBitmap(1393, 'icons')
        self.mask = wx.LIST_MASK_TEXT

    def getText(self, stuff):
        if isinstance(stuff, TargetWrapper):
            em, therm, kin, explo, layer = stuff.getResists(includeLayer=True)
            if stuff.isFit:
                modeSuffixMap = {
                    TargetResistMode.auto: 'auto',
                    TargetResistMode.shield: 'shield',
                    TargetResistMode.armor: 'armor',
                    TargetResistMode.hull: 'hull',
                    TargetResistMode.weightedAverage: 'average'}
                modeSuffix = modeSuffixMap[stuff.resistMode]
                if stuff.resistMode == TargetResistMode.auto and layer is not None:
                    modeSuffix = '{} {}'.format(modeSuffix, layer)
                modeSuffix = ' ({})'.format(modeSuffix)
            else:
                modeSuffix = ''
            return '{}/{}/{}/{}{}'.format(
                formatAmount(val=em * 100, prec=3, lowest=0, highest=0),
                formatAmount(val=therm * 100, prec=3, lowest=0, highest=0),
                formatAmount(val=kin * 100, prec=3, lowest=0, highest=0),
                formatAmount(val=explo * 100, prec=3, lowest=0, highest=0),
                modeSuffix)
        return ''

    def getToolTip(self, mod):
        return 'Target resistances\nEM / Thermal / Kinetic / Explosive'


TargetResists.register()
