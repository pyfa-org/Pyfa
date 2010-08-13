#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx.aui
from gui.fittingView import FittingView
from gui.statsPane import StatsPane

class FitMultiSwitch(wx.aui.AuiNotebook):
    def __init__(self, parent):
        wx.aui.AuiNotebook.__init__(self, parent, wx.ID_ANY)
        self.closeButtonActiveflag = self.GetWindowStyleFlag()
        self.closeButtonInactiveFlag &= ~(wx.aui.AUI_NB_CLOSE_BUTTON | wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB | wx.aui.AUI_NB_CLOSE_ON_ALL_TABS)
        self.SetArtProvider(wx.aui.AuiSimpleTabArt())
        self.AddPage(wx.Panel(self), "+")
        self.SetBackgroundColour(parent.GetBackgroundColour())

    def AddTab(self):
        p = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer.Add(FittingView(p), 1, wx.EXPAND)
        sizer.Add(StatsPane(p), 0, wx.EXPAND)

        p.SetSizer(sizer)
        pos = self.GetPageCount() - 1
        self.InsertPage(pos, p, "Empty tab")
        self.SetSelection(pos)
