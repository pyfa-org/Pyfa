# coding: utf-8
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
from logbook import Logger

import gui.mainFrame
from eos.saveddata.fit import Fit
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn


pyfalog = Logger(__name__)


class ProjectionRangeColumn(ViewColumn):

    name = 'Projection Range'

    def __init__(self, fittingView, params):
        super().__init__(fittingView)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.imageId = fittingView.imageList.GetImageIndex(1391, "icons")
        self.bitmap = BitmapLoader.getBitmap(1391, "icons")
        self.mask = wx.LIST_MASK_IMAGE

    def getText(self, stuff):
        if isinstance(stuff, Fit):
            fitID = self.mainFrame.getActiveFit()
            info = stuff.getProjectionInfo(fitID)
            projRange = info.projectionRange
        else:
            projRange = getattr(stuff, 'projectionRange', None)
        if projRange is None:
            return ''
        return formatAmount(projRange, 3, 0, 3, unitName='m')

    def getToolTip(self, mod):
        return 'Projection Range'


ProjectionRangeColumn.register()
