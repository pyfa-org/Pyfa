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

from graphs.style import BASE_COLORS
from graphs.wrapper import SourceWrapper
from gui.viewColumn import ViewColumn


class GraphColor(ViewColumn):

    name = 'Graph Color'

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.resizable = False
        self.size = 24
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_TEXT

    def getImageId(self, stuff):
        if isinstance(stuff, SourceWrapper):
            try:
                colorData = BASE_COLORS[stuff.colorID]
            except KeyError:
                return -1
            img = self.fittingView.imageList.GetImageIndex(colorData.iconName, 'gui')
            return img
        return -1

    def getToolTip(self, stuff):
        if isinstance(stuff, SourceWrapper):
            return 'Change line color'
        return ''


GraphColor.register()
