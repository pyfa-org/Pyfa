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
from gui.preferenceView import PreferenceView
from gui.bitmapLoader import BitmapLoader


class PreferenceDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetTitle("pyfa - Preferences")
        i = wx.IconFromBitmap(BitmapLoader.getBitmap("preferences_small", "gui"))
        self.SetIcon(i)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.listbook = wx.Listbook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT)

        self.listview = self.listbook.GetListView()
        # self.listview.SetMinSize((500, -1))
        # self.listview.SetSize((500, -1))

        self.imageList = wx.ImageList(32, 32)
        self.listbook.SetImageList(self.imageList)

        mainSizer.Add(self.listbook, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline2, 0, wx.EXPAND, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        self.btnOK = wx.Button(self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnOK, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.EXPAND, 5)
        self.SetSizer(mainSizer)

        self.Centre(wx.BOTH)

        for prefView in PreferenceView.views:
            page = wx.Panel(self.listbook)
            bmp = prefView.getImage()
            if bmp:
                imgID = self.imageList.Add(bmp)
            else:
                imgID = -1
            prefView.populatePanel(page)
            self.listbook.AddPage(page, prefView.title, imageId=imgID)

        # Set the height based on a condition. Can all the panels fit in the current height?
        # If not, use the .GetBestVirtualSize() to ensure that all content is available.
        minHeight = 550
        bestFit = self.GetBestVirtualSize()
        if minHeight > bestFit[1]:
            self.SetSizeWH(650, minHeight)
        else:
            self.SetSizeWH(650, bestFit[1])

        self.Layout()

        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOK)

    def OnBtnOK(self, event):
        self.Close()
