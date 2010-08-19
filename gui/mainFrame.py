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
from gui.mainMenuBar import MainMenuBar
from gui.mainToolBar import MainToolBar
from gui.marketBrowser import MarketBrowser
from gui.fitMultiSwitch import FitMultiSwitch
from gui.statsPane import StatsPane
from gui.shipBrowser import ShipBrowser
from wx.lib.wordwrap import wordwrap
import aboutData

class MainFrame(wx.Frame):
    __instance = None
    @classmethod
    def getInstance(cls):
        return cls.__instance if cls.__instance is not None else MainFrame()

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="pyfa - Python Fitting Assistant")
        MainFrame.__instance = self

        self.SetMinSize((1000, 700))
        self.setSize((1000, 700))

        #Register menubar events / only quit for now
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        marketShipBrowserPanel = wx.Panel(self.splitter)
        self.marketShipBrowserSizer = wx.BoxSizer(wx.VERTICAL)
        marketShipBrowserPanel.SetSizer(self.marketShipBrowserSizer)

        self.marketBrowser = MarketBrowser(marketShipBrowserPanel)
        self.marketShipBrowserSizer.Add(self.marketBrowser, 1, wx.EXPAND)


        self.shipBrowser = ShipBrowser(marketShipBrowserPanel)
        self.marketShipBrowserSizer.Add(self.shipBrowser, 1, wx.EXPAND)

        statsFitviewPanel = wx.Panel(self.splitter)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        statsFitviewPanel.SetSizer(sizer)

        self.fitMultiSwitch = FitMultiSwitch(statsFitviewPanel)
        self.fitMultiSwitch.AddTab()

        self.statsPane = StatsPane(statsFitviewPanel)

        sizer.Add(self.fitMultiSwitch, 1, wx.EXPAND)
        sizer.Add(self.statsPane, 0, wx.EXPAND)

        self.splitter.SplitVertically(marketShipBrowserPanel, statsFitviewPanel)
        self.splitter.SetMinimumPaneSize(10)
        self.splitter.SetSashPosition(300)

        #Add menu
        self.SetMenuBar(MainMenuBar())
        self.SetToolBar(MainToolBar(self))

        #Show ourselves
        self.Show()

    def ExitApp(self, evt):
        self.Close()

    def ShowAboutBox(self, evt):
       info = wx.AboutDialogInfo()
       info.Name = "pyfa"
       info.Version = aboutData.versionString
       info.Description = wordwrap(aboutData.description + "\n\n\nDevelopers: " + ", ".join(aboutData.developers) + "\nLicense: " + aboutData.license + " see included " + aboutData.licenseLocation,
           350, wx.ClientDC(self))
       info.WebSite = ("http://pyfa.sourceforge.net/", "pyfa home page")
       wx.AboutBox(info)
