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

import wx

class MarketBrowser(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        vbox.Add(self.splitter, 1, wx.EXPAND)
        hbox.Add(vbox, 1, wx.EXPAND)
        self.SetSizer(hbox)

        self.marketView = wx.TreeCtrl(self.splitter)
        self.itemView = wx.TreeCtrl(self.splitter)

        self.splitter.SplitHorizontally(self.marketView, self.itemView)
        self.splitter.SetMinimumPaneSize(400)
