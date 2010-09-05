#===============================================================================
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
#===============================================================================

from gui import builtinViewColumns
from gui.viewColumn import ViewColumn
import gui.mainFrame
import wx

class DroneCheckbox(ViewColumn):
    name = "Drone Checkbox"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.resizable = False
        self.size = 24
        for name, state in (("checked", wx.CONTROL_CHECKED), ("unchecked", 0)):
            bitmap = wx.EmptyBitmap(16, 16)
            dc = wx.MemoryDC()
            dc.SelectObject(bitmap)
            dc.SetBackground(wx.TheBrushList.FindOrCreateBrush(fittingView.GetBackgroundColour(), wx.SOLID))
            dc.Clear()
            wx.RendererNative.Get().DrawCheckBox(fittingView, dc, wx.Rect(0, 0, 16, 16), state)
            dc.Destroy()
            setattr(self, "%sId" % name, fittingView.imageList.Add(bitmap))

    def getText(self, mod):
        return ""

    def getImageId(self, drone):
        if drone.amountActive > 0:
            return self.checkedId
        else:
            return self.uncheckedId

builtinViewColumns.registerColumn(DroneCheckbox)
