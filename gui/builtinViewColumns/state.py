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

from gui.viewColumn import ViewColumn
from gui import bitmapLoader
import wx
from eos.types import Drone, Module
from eos.types import State as State_

class State(ViewColumn):
    name = "State"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.resizable = False
        self.size = 16
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_IMAGE
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

    def getImageId(self, stuff):
        if isinstance(stuff, Drone):
            return self.checkedId if stuff.amountActive > 0 else self.uncheckedId
        elif isinstance(stuff, Module):
            if stuff.isEmpty:
                return -1
            else:
                bitmap = bitmapLoader.getBitmap("state_%s_small" % State_.getName(stuff.state).lower(), "icons")
                return self.fittingView.imageList.Add(bitmap)
        else:
            active = getattr(stuff, "active", None)
            if active is None:
                return -1
            else:
                return self.checkedId if active else self.uncheckedId

State.register()
