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
from gui.bitmap_loader import BitmapLoader

_t = wx.GetTranslation

class PreferenceDialog(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        self.SetTitle("pyfa - " + _t("Preferences"))
        i = wx.Icon(BitmapLoader.getBitmap("preferences_small", "gui"))
        self.SetIcon(i)
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.listbook = wx.Listbook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT)

        self.listview = self.listbook.GetListView()
        # self.listview.SetMinSize((500, -1))
        # self.listview.SetSize((500, -1))

        self.imageList = wx.ImageList(32, 32)
        self.listbook.AssignImageList(self.imageList)

        mainSizer.Add(self.listbook, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT, 5)

        self.m_staticline2 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        mainSizer.Add(self.m_staticline2, 0, wx.EXPAND, 5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()
        # localization todo: "OK" button shoudl be a built in thing that is already localized...
        self.btnOK = wx.Button(self, wx.ID_ANY, "OK", wx.DefaultPosition, wx.DefaultSize, 0)
        btnSizer.Add(self.btnOK, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.EXPAND, 5)
        self.SetSizer(mainSizer)

        self.Centre(wx.BOTH)

        for prefView in PreferenceView.views:
            page = wx.ScrolledWindow(self.listbook)
            page.SetScrollRate(15, 15)
            bmp = prefView.getImage()
            if bmp:
                imgID = self.imageList.Add(bmp)
            else:
                imgID = -1
            prefView.populatePanel(page)

            self.listbook.AddPage(page, prefView.title, imageId=imgID)

        bestFit = self.GetBestVirtualSize()
        width = max(bestFit[0], 800 if "wxGTK" in wx.PlatformInfo else 650)
        height = max(bestFit[1], 550)
        self.SetSize(width, height)

        self.Layout()

        self.Bind(wx.EVT_CHAR_HOOK, self.kbEvent)
        self.btnOK.Bind(wx.EVT_BUTTON, self.OnBtnOK)

    def OnBtnOK(self, event):
        self.Close()

    def kbEvent(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and event.GetModifiers() == wx.MOD_NONE:
            self.Close()
            return
        event.Skip()
