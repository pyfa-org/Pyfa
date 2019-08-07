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

from graphs.style import LIGHTNESSES
from graphs.wrapper import TargetWrapper
from gui.viewColumn import ViewColumn


class GraphLightness(ViewColumn):

    name = 'Graph Lightness'

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.resizable = False
        self.size = 24
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_TEXT

    def getImageId(self, stuff):
        if isinstance(stuff, TargetWrapper):
            try:
                lightnessData = LIGHTNESSES[stuff.lightnessID]
            except KeyError:
                return -1
            img = self.fittingView.imageList.GetImageIndex(lightnessData.iconName, 'gui')
            return img
        return -1

    def getToolTip(self, stuff):
        if isinstance(stuff, TargetWrapper):
            return 'Change line brightness'
        return ''


GraphLightness.register()
