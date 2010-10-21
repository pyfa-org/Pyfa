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
from gui.preferenceView import PreferenceView
class PreferenceDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, size=wx.Size(600, 400), style=wx.DEFAULT_DIALOG_STYLE)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.listbook = wx.Listbook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT)
        self.listbook.GetListView().SetMinSize((500, -1))
        self.listbook.GetListView().SetSize((500, -1))

        mainSizer.Add(self.listbook, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(mainSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        for title, prefView in PreferenceView.views.iteritems():
            page = wx.Panel(self.listbook)
            prefView.populatePanel(page)
            self.listbook.AddPage(page, title)
