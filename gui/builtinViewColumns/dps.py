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

import eos.config
import gui.mainFrame
from eos.saveddata.fit import Fit
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from gui.bitmap_loader import BitmapLoader
from gui.viewColumn import ViewColumn
from gui.utils.numberFormatter import formatAmount


class DpsColumn(ViewColumn):

    name = 'Dps'

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.imageId = fittingView.imageList.GetImageIndex(1432, 'icons')
        self.bitmap = BitmapLoader.getBitmap(1432, 'icons')
        self.mask = wx.LIST_MASK_TEXT

    def getText(self, stuff):
        if isinstance(stuff, Fit):
            defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
            dps = stuff.getTotalDps(spoolOptions=SpoolOptions(SpoolType.SCALE, defaultSpoolValue, False)).total
            if dps is None:
                return ''
            return formatAmount(dps, 3, 0, 0)
        return ''

    def getToolTip(self, stuff):
        return 'Declared DPS'


DpsColumn.register()
