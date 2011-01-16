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

import sys
import os.path

import sqlalchemy
import wx

from wx._core import PyDeadObjectError
from wx.lib.wordwrap import wordwrap

import service
import config

import gui.aboutData
import gui.chromeTabs
import gui.utils.animUtils as animUtils

from gui import bitmapLoader
from gui.mainMenuBar import MainMenuBar
from gui.additionsPane import AdditionsPane
from gui.marketBrowser import MarketBrowser
from gui.multiSwitch import MultiSwitch
from gui.statsPane import StatsPane
from gui.shipBrowser import ShipBrowser, FitSelected
from gui.characterEditor import CharacterEditor
from gui.characterSelection import CharacterSelection
from gui.patternEditor import DmgPatternEditorDlg
from gui.preferenceDialog import PreferenceDialog
from gui.graphFrame import GraphFrame
from gui.copySelectDialog import CopySelectDialog
from gui.utils.clipboard import toClipboard, fromClipboard
from gui.fleetBrowser import FleetBrowser
from builtinViews import *

#dummy panel no paint no erasebk
class PFPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnBkErase)

    def OnPaint(self, event):
        event.Skip()
    def OnBkErase(self, event):
        pass

class MainFrame(wx.Frame):
    __instance = None
    @classmethod
    def getInstance(cls):
        return cls.__instance if cls.__instance is not None else MainFrame()

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="pyfa - Python Fitting Assistant")
        MainFrame.__instance = self

        self.LoadMainFrameAttribs()

        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        i = wx.IconFromBitmap(bitmapLoader.getBitmap("pyfa", "icons"))
        self.SetIcon(i)


        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        mainSizer.Add(self.splitter,1,wx.EXPAND | wx.LEFT, 2)

        self.FitviewAdditionsPanel = PFPanel(self.splitter)
        faSizer = wx.BoxSizer(wx.VERTICAL)

        self.fitMultiSwitch = MultiSwitch(self.FitviewAdditionsPanel)

        faSizer.Add(self.fitMultiSwitch,1,wx.EXPAND)

        self.additionsPane = AdditionsPane(self.FitviewAdditionsPanel)
        faSizer.Add(self.additionsPane, 0, wx.EXPAND)

        self.FitviewAdditionsPanel.SetSizer(faSizer)


        self.notebookBrowsers = gui.chromeTabs.PFNotebook(self.splitter, False)

        self.marketBrowser = MarketBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.marketBrowser, "Market", showClose = False)

        self.shipBrowser = ShipBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.shipBrowser, "Ships", showClose = False)

        #=======================================================================
        # DISABLED FOR RC2 RELEASE
        self.fleetBrowser = FleetBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.fleetBrowser, "Fleets", showClose = False)
        #=======================================================================

        self.notebookBrowsers.SetSelection(1)

        self.splitter.SplitVertically(self.notebookBrowsers, self.FitviewAdditionsPanel)
        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SetSashPosition(300)

        cstatsSizer = wx.BoxSizer(wx.VERTICAL)

        self.charSelection = CharacterSelection(self)
        cstatsSizer.Add(self.charSelection, 0, wx.EXPAND)

        self.statsPane = StatsPane(self)
        cstatsSizer.Add(self.statsPane, 0, wx.EXPAND)

        mainSizer.Add(cstatsSizer, 0 , wx.EXPAND)

        self.SetSizer(mainSizer)

        self.addPageId = wx.NewId()
        self.closePageId = wx.NewId()

        self.graphFrame = None
        self.statsWnds = []
        self.activeStatsWnd = None

        #Add menu
        self.SetMenuBar(MainMenuBar())
        #self.SetToolBar(MainToolBar(self))

        self.registerMenu()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #Show ourselves
        self.Show()

    def LoadMainFrameAttribs(self):

        mainFrameDefaultAttribs = {"wnd_width":1000, "wnd_height": 700, "wnd_maximized": False}
        self.mainFrameAttribs = service.SettingsProvider.getInstance().getSettings("pyfaMainWindowAttribs", mainFrameDefaultAttribs)
        if self.mainFrameAttribs["wnd_maximized"]:
            width = mainFrameDefaultAttribs["wnd_width"]
            height = mainFrameDefaultAttribs["wnd_height"]
            self.Maximize()
        else:
            width = self.mainFrameAttribs["wnd_width"]
            height = self.mainFrameAttribs["wnd_height"]

        self.SetSize((width, height))
        self.SetMinSize((mainFrameDefaultAttribs["wnd_width"], mainFrameDefaultAttribs["wnd_height"]))

    def UpdateMainFrameAttribs(self):
        if self.IsIconized():
            return
        width,height = self.GetSize()

        self.mainFrameAttribs["wnd_width"] = width
        self.mainFrameAttribs["wnd_height"] = height
        self.mainFrameAttribs["wnd_maximized"] = self.IsMaximized()

    def SetActiveStatsWindow(self, wnd):
        self.activeStatsWnd = wnd

    def GetActiveStatsWindow(self):

        if self.activeStatsWnd in self.statsWnds:
            return self.activeStatsWnd

        if len(self.statsWnds) > 0:
            return self.statsWnds[len(self.statsWnds) - 1]
        else:
            return None

    def RegisterStatsWindow(self, wnd):
        self.statsWnds.append(wnd)

    def UnregisterStatsWindow(self, wnd):
        self.statsWnds.remove(wnd)

    def getActiveFit(self):
        p = self.fitMultiSwitch.GetSelectedPage()
        m = getattr(p, "getActiveFit", None)
        return m() if m is not None else None

    def getActiveView(self):
        sel = self.fitMultiSwitch.GetSelectedPage()

    def CloseCurrentPage(self, evt):
        ms = self.fitMultiSwitch

        page = ms.GetSelection()
        if page is not None:
            ms.DeletePage(page)

    def OnClose(self, event):
        self.UpdateMainFrameAttribs()
        service.SettingsProvider.getInstance().saveAll()
        event.Skip()

    def ExitApp(self, event):
        self.Close()
        event.Skip()

    def ShowAboutBox(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = "pyfa"
        info.Version = gui.aboutData.versionString
        info.Description = wordwrap(gui.aboutData.description + "\n\n\nDevelopers: " +
                                     "".join(gui.aboutData.developers) +
                                     "\n\nAdditional credits:\n  " +
                                     "\n  ".join(gui.aboutData.credits)
                                     + "\n\nLicense: " +
                                     gui.aboutData.license +
                                     " - see included " +
                                     gui.aboutData.licenseLocation +
                                     "\n\nPython: \t" + sys.version +
                                     "\nwxPython: \t" + wx.__version__ +
                                     "\nSQLAlchemy: \t" + sqlalchemy.__version__,
            700, wx.ClientDC(self))
        info.WebSite = ("http://www.evefit.org/Pyfa", "pyfa home page")
        wx.AboutBox(info)


    def showCharacterEditor(self, event):
        dlg=CharacterEditor(self)
        dlg.Show()

    def showDamagePatternEditor(self, event):
        dlg=DmgPatternEditorDlg(self)
        dlg.ShowModal()
        dlg.Destroy()

    def showImportDialog(self, event):
        fits = []
        sFit = service.Fit.getInstance()
        dlg=wx.FileDialog(
            self,
            "Open One Or More Fitting Files",
            wildcard = "EFT text fitting files (*.cfg)|*.cfg|EvE XML fitting files (*.xml)|*.xml|All Files (*)|*",
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if (dlg.ShowModal() == wx.ID_OK):
            try:
                for importPath in dlg.GetPaths():
                    fits += sFit.importFit(importPath)
                IDs = sFit.saveImportedFits(fits)
                self._openAfterImport(len(fits), IDs)
            except:
                wx.MessageBox("Error importing from file.", "Error", wx.OK | wx.ICON_ERROR, self)
        dlg.Destroy()

    def _openAfterImport(self, importCount, fitIDs):
        if importCount == 1:
            if self.getActiveFit() != fitIDs[0]:
                wx.PostEvent(self, FitSelected(fitID=fitIDs[0]))
        self.shipBrowser.RefreshContent()
    def showExportDialog(self, event):
        dlg=wx.FileDialog(
            self,
            "Save Fitting As...",
            wildcard = "EFT text fitting files (*.cfg)|*.cfg|EvE XML fitting files (*.xml)|*.xml",
            style = wx.FD_SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            sFit = service.Fit.getInstance()
            format = dlg.GetFilterIndex()
            output = ""
            path = dlg.GetPath()
            if (format == 0):
                output = sFit.exportFit(self.getActiveFit())
                if '.' not in os.path.basename(path):
                    path += ".cfg"
            elif (format == 1):
                output = sFit.exportXml(self.getActiveFit())
                if '.' not in os.path.basename(path):
                    path += ".xml"
            else:
                print "oops, invalid fit format %d" % format
                dlg.Destroy()
                return
            file = open(path, "w")
            file.write(output)
            file.close()
        dlg.Destroy()

    def showPreferenceDialog(self, event):
        dlg = PreferenceDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def registerMenu(self):
        menuBar = self.GetMenuBar()
        # Quit
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        # Widgets Inspector
        if config.debug:
            self.Bind(wx.EVT_MENU, self.openWXInspectTool, id=911)
        # About
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)
        # Char editor
        self.Bind(wx.EVT_MENU, self.showCharacterEditor, id=menuBar.characterEditorId)
        # Damage pattern editor
        self.Bind(wx.EVT_MENU, self.showDamagePatternEditor, id=menuBar.damagePatternEditorId)
        # Import dialog
        self.Bind(wx.EVT_MENU, self.showImportDialog, id=wx.ID_OPEN)
        # Export dialog
        self.Bind(wx.EVT_MENU, self.showExportDialog, id=wx.ID_SAVEAS)
        # Import from Clipboard
        self.Bind(wx.EVT_MENU, self.importFromClipboard, id=wx.ID_PASTE)
        # Backup fits
        self.Bind(wx.EVT_MENU, self.backupToXml, id=menuBar.backupFitsId)
        # Preference dialog
        self.Bind(wx.EVT_MENU, self.showPreferenceDialog, id = menuBar.preferencesId)

        #Clipboard exports
        self.Bind(wx.EVT_MENU, self.exportToClipboard, id=wx.ID_COPY)

        #Graphs
        self.Bind(wx.EVT_MENU, self.openGraphFrame, id=menuBar.graphFrameId)

        toggleShipMarketId = wx.NewId()
        ctabnext = wx.NewId()
        ctabprev = wx.NewId()

        self.additionstab1 = wx.NewId()
        self.additionstab2 = wx.NewId()
        self.additionstab3 = wx.NewId()
        self.additionstab4 = wx.NewId()

        # Close Page
        self.Bind(wx.EVT_MENU, self.CloseCurrentPage, id=self.closePageId)
        self.Bind(wx.EVT_MENU, self.HAddPage, id = self.addPageId)
        self.Bind(wx.EVT_MENU, self.toggleShipMarket, id = toggleShipMarketId)
        self.Bind(wx.EVT_MENU, self.CTabNext, id = ctabnext)
        self.Bind(wx.EVT_MENU, self.CTabPrev, id = ctabprev)

        self.Bind(wx.EVT_MENU, self.AdditionsTabSelect, id = self.additionstab1)
        self.Bind(wx.EVT_MENU, self.AdditionsTabSelect, id = self.additionstab2)
        self.Bind(wx.EVT_MENU, self.AdditionsTabSelect, id = self.additionstab3)
        self.Bind(wx.EVT_MENU, self.AdditionsTabSelect, id = self.additionstab4)

        actb = [(wx.ACCEL_CTRL, ord('T'), self.addPageId),
                (wx.ACCEL_CMD, ord('T'), self.addPageId),

                (wx.ACCEL_CTRL, ord("W"), self.closePageId),
                (wx.ACCEL_CMD, ord("W"), self.closePageId),

                (wx.ACCEL_CTRL, ord(" "), toggleShipMarketId),
                (wx.ACCEL_CMD, ord(" "), toggleShipMarketId),

                (wx.ACCEL_CTRL, wx.WXK_TAB, ctabnext),
                (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_TAB, ctabprev),
                (wx.ACCEL_CMD, wx.WXK_TAB, ctabnext),
                (wx.ACCEL_CMD | wx.ACCEL_SHIFT, wx.WXK_TAB, ctabprev),

                (wx.ACCEL_CTRL, ord('1'), self.additionstab1),
                (wx.ACCEL_CTRL, ord('2'), self.additionstab2),
                (wx.ACCEL_CTRL, ord('3'), self.additionstab3),
                (wx.ACCEL_CTRL, ord('4'), self.additionstab4),
                (wx.ACCEL_CMD, ord('1'), self.additionstab1),
                (wx.ACCEL_CMD, ord('2'), self.additionstab2),
                (wx.ACCEL_CMD, ord('3'), self.additionstab3),
                (wx.ACCEL_CMD, ord('4'), self.additionstab4)
                ]
        atable = wx.AcceleratorTable(actb)
        self.SetAcceleratorTable(atable)

    def AdditionsTabSelect(self, event):
        selTab = None
        if event.GetId() == self.additionstab1:
            selTab = 0
        if event.GetId() == self.additionstab2:
            selTab = 1
        if event.GetId() == self.additionstab3:
            selTab = 2
        if event.GetId() == self.additionstab4:
            selTab = 3

        if selTab is not None:
            self.additionsPane.notebook.SetSelection(selTab)

    def CTabNext(self, event):
        self.fitMultiSwitch.NextPage()

    def CTabPrev(self, event):
        self.fitMultiSwitch.PrevPage()

    def HAddPage(self,event):
        self.fitMultiSwitch.AddPage(wx.Panel(self, size = (0,0)), "Empty Tab")

    def toggleShipMarket(self, event):
        sel = self.notebookBrowsers.GetSelection()
        self.notebookBrowsers.SetSelection(0 if sel == 1 else 1)

    def clipboardEft(self):
        sFit = service.Fit.getInstance()
        toClipboard(sFit.exportFit(self.getActiveFit()))

    def clipboardDna(self):
        sFit = service.Fit.getInstance()
        toClipboard(sFit.exportDna(self.getActiveFit()))

    def clipboardXml(self):
        sFit = service.Fit.getInstance()
        toClipboard(sFit.exportXml(self.getActiveFit()))

    def importFromClipboard(self, event):
        sFit = service.Fit.getInstance()
        try:
            fits = sFit.importFitFromBuffer(fromClipboard())
            IDs = sFit.saveImportedFits(fits)
            self._openAfterImport(len(fits), IDs)
        except:
            pass

    def exportToClipboard(self, event):
        CopySelectDict = {CopySelectDialog.copyFormatEft: self.clipboardEft,
                          CopySelectDialog.copyFormatXml: self.clipboardXml,
                          CopySelectDialog.copyFormatDna: self.clipboardDna}
        dlg = CopySelectDialog(self)
        dlg.ShowModal()
        selected = dlg.GetSelected()
        try:
            CopySelectDict[selected]()
        except:
            pass
        dlg.Destroy()

    def backupToXml(self, event):
        sFit = service.Fit.getInstance()
        saveDialog = wx.FileDialog(
            self,
            "Save Backup As...",
            wildcard = "EvE XML fitting file (*.xml)|*.xml",
            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (saveDialog.ShowModal() == wx.ID_OK):
            filePath = saveDialog.GetPath()
            if '.' not in os.path.basename(filePath):
                filePath += ".xml"
            self.waitDialog = WaitDialog(self)
            sFit.backupFits(filePath, self.closeWaitDialog)
            self.waitDialog.ShowModal()

        saveDialog.Destroy()

    def closeWaitDialog(self):
        self.waitDialog.Destroy()

    def openGraphFrame(self, event):
        if not self.graphFrame:
            self.graphFrame = GraphFrame(self)
            if gui.graphFrame.enabled:
                self.graphFrame.Show()
        else:
            self.graphFrame.SetFocus()

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


class WaitDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"Please wait ...", size=(300,30),
                           style=wx.NO_BORDER)
        mainSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.progress = animUtils.LoadAnimation(self,label = "Processing", size=(300,30))
        mainSizer.Add( self.progress, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
        self.SetSizer( mainSizer )
        self.Layout()
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.CenterOnParent()

    def OnClose(self, event):
        pass
