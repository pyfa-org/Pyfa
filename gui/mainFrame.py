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
from gui import bitmapLoader
from gui.mainMenuBar import MainMenuBar
from gui.additionsPane import AdditionsPane
from gui.marketBrowser import MarketBrowser
from gui.multiSwitch import MultiSwitch
from gui.statsPane import StatsPane
from gui.shipBrowser import ShipBrowser
from wx.lib.wordwrap import wordwrap
from gui.characterEditor import CharacterEditor
import aboutData
from wx._core import PyDeadObjectError

class MainFrame(wx.Frame):
    __instance = None
    @classmethod
    def getInstance(cls):
        return cls.__instance if cls.__instance is not None else MainFrame()

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="pyfa - Python Fitting Assistant")
        MainFrame.__instance = self

        i = wx.IconFromBitmap(bitmapLoader.getBitmap("pyfa", "icons"))
        self.SetIcon(i)

        self.SetMinSize((1000, 700))
        self.SetSize((1000, 700))


        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        self.notebookBrowsers = wx.Notebook(self.splitter, wx.ID_ANY)
        self.notebookBrowsers.Bind(wx.EVT_LEFT_DOWN, self.mouseHit)

        self.marketBrowser = MarketBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.marketBrowser, "Market")

        self.shipBrowser = ShipBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.shipBrowser, "Ships")

        statsFitviewPanel = wx.Panel(self.splitter)
        self.statsSizer = wx.BoxSizer(wx.HORIZONTAL)
        statsFitviewPanel.SetSizer(self.statsSizer)

        self.fittingPanel = wx.Panel(statsFitviewPanel)
        fittingSizer = wx.BoxSizer(wx.VERTICAL)
        self.fittingPanel.SetSizer(fittingSizer)
        self.statsSizer.Add(self.fittingPanel, 1, wx.EXPAND)

        self.fitMultiSwitch = MultiSwitch(self.fittingPanel)
        self.fitMultiSwitch.AddTab()
        fittingSizer.Add(self.fitMultiSwitch, 1, wx.EXPAND)

        self.additionsPane = AdditionsPane(self.fittingPanel)
        fittingSizer.Add(self.additionsPane, 0, wx.EXPAND)


        self.statsPane = StatsPane(statsFitviewPanel)
        self.statsSizer.Add(self.statsPane, 0, wx.EXPAND)

        self.splitter.SplitVertically(self.notebookBrowsers, statsFitviewPanel)
        self.splitter.SetMinimumPaneSize(10)
        self.splitter.SetSashPosition(300)

        #Add menu
        self.SetMenuBar(MainMenuBar())
        #self.SetToolBar(MainToolBar(self))

        self.registerMenu()

        #Show ourselves
        self.Show()

    def getActiveFit(self):
        sel = self.fitMultiSwitch.GetSelection()
        view = self.fitMultiSwitch.GetPage(sel).view
        return view.activeFitID

    def mouseHit(self, event):
        tab, _ = self.notebookBrowsers.HitTest(event.Position)
        if tab != -1:
            self.notebookBrowsers.SetSelection(tab)

    def ExitApp(self, evt):
        try:
            self.Close()
        except PyDeadObjectError:
            pass

    def ShowAboutBox(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = "pyfa"
        info.Version = aboutData.versionString
        info.Description = wordwrap(aboutData.description + "\n\n\nDevelopers: " + ", ".join(aboutData.developers) + "\n\nAdditional credits\n" + "\n".join(aboutData.credits) + "\n\nLicense: " + aboutData.license + " see included " + aboutData.licenseLocation,
            350, wx.ClientDC(self))
        info.WebSite = ("http://pyfa.sourceforge.net/", "pyfa home page")
        wx.AboutBox(info)

    def showCharacterEditor(self, event):
        dlg=CharacterEditor(None)
        dlg.ShowModal()
        dlg.Destroy()

    def registerMenu(self):
        # Quit
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        # Widgets Inspector
        self.Bind(wx.EVT_MENU, self.openWXInspectTool, id=911)
        # About
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)
        # Char editor
        self.Bind(wx.EVT_MENU, self.showCharacterEditor, id=self.GetMenuBar().characterEditorId)

    def toggleShipBrowser(self, event):
        self.GetToolBar().toggleShipBrowser(event)

    def openWXInspectTool(self,event):
        from wx.lib.inspection import InspectionTool
        if not InspectionTool().initialized:
            InspectionTool().Init()

        # Find a widget to be selected in the tree.  Use either the
        # one under the cursor, if any, or this frame.
        wnd = wx.FindWindowAtPointer()
        if not wnd:
            wnd = self
        InspectionTool().Show(wnd, True)

