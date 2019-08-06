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

from graphs.style import BASE_COLORS, LIGHTNESSES
from gui.bitmap_loader import BitmapLoader
from service.const import GraphLightness


class ColorPickerPopup(wx.PopupTransientWindow):

    def __init__(self, parent, wrapper):
        super().__init__(parent, flags=wx.BORDER_SIMPLE)
        self.wrapper = wrapper

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.GridSizer(2, 4, 0, 0)
        self.patches = list()
        for colorID, colorData in BASE_COLORS.items():
            icon = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap(colorData.iconName, 'gui'))
            icon.colorID = colorID
            icon.SetToolTip(colorData.name)
            icon.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            grid.Add(icon, flag=wx.ALL, border=3)
        sizer.Add(grid)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

    def OnLeftDown(self, event):
        colorID = getattr(event.GetEventObject(), 'colorID', None)
        if colorID is not None:
            self.wrapper.colorID = colorID
            self.Parent.OnLineStyleChange()
            self.Hide()
            self.Destroy()
            return
        event.Skip()


class LightnessPickerPopup(wx.PopupTransientWindow):

    def __init__(self, parent, wrapper):
        super().__init__(parent, flags=wx.BORDER_SIMPLE)
        self.wrapper = wrapper

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.GridSizer(1, 3, 0, 0)
        self.patches = list()
        customOrder = (GraphLightness.dark, GraphLightness.normal, GraphLightness.bright)
        for lightnessID in customOrder:
            lightnessData = LIGHTNESSES[lightnessID]
            icon = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap(lightnessData.iconName, 'gui'))
            icon.lightnessID = lightnessID
            icon.SetToolTip(lightnessData.name)
            icon.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            grid.Add(icon, flag=wx.ALL, border=3)
        sizer.Add(grid)

        self.SetSizer(sizer)
        self.Fit()
        self.Layout()

    def OnLeftDown(self, event):
        lightnessID = getattr(event.GetEventObject(), 'lightnessID', None)
        if lightnessID is not None:
            self.wrapper.lightnessID = lightnessID
            self.Parent.OnLineStyleChange()
            self.Hide()
            self.Destroy()
            return
        event.Skip()
