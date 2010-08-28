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

import wx
import gui.mainFrame
import bitmapLoader

class ItemStatsFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,
                          gui.mainFrame.MainFrame.getInstance(),
                          wx.ID_ANY, title="pyfa - Item Stats",
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        i = wx.IconFromBitmap(bitmapLoader.getBitmap("pyfa", "icons"))
        self.SetIcon(i)

        self.SetMinSize((500, 300))
        self.SetSize((500, 300))
        self.SetMaxSize((500, 300))

        self.Show()

class ItemStatsMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)

        self.showInfoId = wx.NewId()
        self.Append(self.showInfoId, "&Item stats", "moo")
        self.Bind(wx.EVT_MENU, self.itemStats, id=self.showInfoId)

    def setItem(self, itemId):
        self.itemId = itemId

    def itemStats(self, event):
        ItemStatsFrame()

