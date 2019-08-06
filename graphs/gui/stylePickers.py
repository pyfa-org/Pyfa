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

from graphs.style import BASE_COLORS, LIGHTNESSES, STYLES
from gui.bitmap_loader import BitmapLoader
from service.const import GraphLightness


class StylePickerPopup(wx.PopupTransientWindow):

    def __init__(self, parent, wrapper):
        super().__init__(parent, flags=wx.BORDER_SIMPLE)
        self.wrapper = wrapper

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.GridSizer(self.nrows, self.ncols, 0, 0)
        self.patches = list()
        for styleID in self.sortingOrder:
            styleData = self.styleContainer[styleID]
            icon = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap(styleData.iconName, 'gui'))
            icon.styleID = styleID
            icon.SetToolTip(styleData.name)
            icon.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            grid.Add(icon, flag=wx.ALL, border=3)
        sizer.Add(grid)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

    @property
    def styleContainer(self):
        raise NotImplementedError

    @property
    def sortingOrder(self):
        return self.styleContainer

    @property
    def ncols(self):
        raise NotImplementedError

    @property
    def nrows(self):
        raise NotImplementedError

    @property
    def wrapperAttr(self):
        raise NotImplementedError

    def OnLeftDown(self, event):
        styleID = getattr(event.GetEventObject(), 'styleID', None)
        if styleID is not None:
            setattr(self.wrapper, self.wrapperAttr, styleID)
            self.Parent.OnLineStyleChange()
            self.Hide()
            self.Destroy()
            return
        event.Skip()


class ColorPickerPopup(StylePickerPopup):

    styleContainer = BASE_COLORS
    wrapperAttr = 'colorID'
    ncols = 4
    nrows = 2


class LightnessPickerPopup(StylePickerPopup):

    styleContainer = LIGHTNESSES
    sortingOrder = (GraphLightness.dark, GraphLightness.normal, GraphLightness.bright)
    wrapperAttr = 'lightnessID'
    ncols = 3
    nrows = 1


class LineStylePickerPopup(StylePickerPopup):

    styleContainer = STYLES
    wrapperAttr = 'lineStyleID'
    ncols = 4
    nrows = 1
