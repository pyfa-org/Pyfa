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

from eos.saveddata.fit import Fit
from graphs.wrapper import BaseWrapper
from gui.bitmap_loader import BitmapLoader
from eos.utils.float import floatUnerr
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn


class DampScanResColumn(ViewColumn):

    name = 'Damp ScanRes'

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.imageId = fittingView.imageList.GetImageIndex(74, 'icons')
        self.bitmap = BitmapLoader.getBitmap(74, 'icons')
        self.mask = wx.LIST_MASK_IMAGE

    def getText(self, stuff):
        if isinstance(stuff, BaseWrapper):
            stuff = stuff.item
        mult = 1
        if isinstance(stuff, Fit):
            mult = floatUnerr(stuff.getDampMultScanRes())
        if mult == 1:
            text = ''
        else:
            text = '{}%'.format(formatAmount((mult - 1) * 100, 3, 0, 0, forceSign=True))
        return text

    def getImageId(self, stuff):
        return -1

    def getToolTip(self, stuff):
        return 'Scan resolution dampening'


DampScanResColumn.register()
