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

from graphs.colors import BASE_COLORS
from gui.bitmap_loader import BitmapLoader


class ColorPickerPopup(wx.PopupTransientWindow):

    def __init__(self, parent, wrapper, ncol=0, nrow=0):
        super().__init__(parent, flags=wx.BORDER_STATIC)
        self.wrapper = wrapper
        ncol = ncol or len(BASE_COLORS)
        nrow = nrow or int(len(BASE_COLORS) / ncol) + (1 if (len(BASE_COLORS) % ncol) else 0)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        grid = wx.GridSizer(nrow, ncol, 0, 0)
        self.patches = list()
        for colorID, colorData in BASE_COLORS.items():
            icon = wx.StaticBitmap(self, wx.ID_ANY, BitmapLoader.getBitmap(colorData.iconName, 'gui'))
            icon.colorID = colorID
            icon.SetToolTip(colorData.name)
            icon.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            grid.Add(icon, flag=wx.ALL, border=3)

        sizer.Add(grid)
        sizer.Fit(self)
        self.Layout()

    def OnLeftDown(self, event):
        colorID = getattr(event.GetEventObject(), 'colorID', None)
        if colorID is not None:
            self.wrapper.colorID = colorID
            self.Parent.OnColorChange()
            self.Hide()
            self.Destroy()
            return
        event.Skip()
