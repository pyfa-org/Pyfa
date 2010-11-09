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
import service
from gui import bitmapLoader
from gui.mainMenuBar import MainMenuBar
from gui.additionsPane import AdditionsPane
from gui.marketBrowser import MarketBrowser
from gui.multiSwitch import MultiSwitch
from gui.statsPane import StatsPane
from gui.shipBrowser import ShipBrowser, FitSelected
from wx.lib.wordwrap import wordwrap
from gui.characterEditor import CharacterEditor
from gui.characterSelection import CharacterSelection
from gui.patternEditor import DmgPatternEditorDlg
from gui.preferenceDialog import PreferenceDialog
from gui.graphFrame import GraphFrame
from gui.copySelectDialog import CopySelectDialog
import aboutData
import gui.fittingView as fv
from wx._core import PyDeadObjectError
import os.path

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

        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        i = wx.IconFromBitmap(bitmapLoader.getBitmap("pyfa", "icons"))
        self.SetIcon(i)

        self.SetMinSize((1000, 700))
        self.SetSize((1000, 700))

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.splitter = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)

        mainSizer.Add(self.splitter,1,wx.EXPAND | wx.LEFT, 2)

        self.FitviewAdditionsPanel = PFPanel(self.splitter)
        faSizer = wx.BoxSizer(wx.VERTICAL)

        self.fitMultiSwitch = MultiSwitch(self.FitviewAdditionsPanel)
        self.fitMultiSwitch.AddTab()
        faSizer.Add(self.fitMultiSwitch,1,wx.EXPAND)

        self.additionsPane = AdditionsPane(self.FitviewAdditionsPanel)
        faSizer.Add(self.additionsPane, 0, wx.EXPAND)

        self.FitviewAdditionsPanel.SetSizer(faSizer)

        self.notebookBrowsers = wx.Notebook(self.splitter, wx.ID_ANY)
        self.notebookBrowsers.Bind(wx.EVT_LEFT_DOWN, self.mouseHit)

        self.marketBrowser = MarketBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.marketBrowser, "Market")

        self.shipBrowser = ShipBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.shipBrowser, "Ships")
        self.notebookBrowsers.SetSelection(1)

        self.splitter.SplitVertically(self.notebookBrowsers, self.FitviewAdditionsPanel)
        self.splitter.SetMinimumPaneSize(200)
        self.splitter.SetSashPosition(300)

        cstatsSizer = wx.BoxSizer(wx.VERTICAL)

        self.charSelection = CharacterSelection(self)
        cstatsSizer.Add(self.charSelection, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT , 3)

        self.statsPane = StatsPane(self)
        cstatsSizer.Add(self.statsPane, 0, wx.EXPAND)

        mainSizer.Add(cstatsSizer, 0 , wx.EXPAND)

        self.SetSizer(mainSizer)

        self.addTabId = wx.NewId()
        self.closeTabId = wx.NewId()

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

    def getFittingView(self):
        sel = self.fitMultiSwitch.GetSelection()
        return self.fitMultiSwitch.GetPage(sel).view

    def mouseHit(self, event):
        tab, _ = self.notebookBrowsers.HitTest(event.Position)
        if tab != -1:
            self.notebookBrowsers.SetSelection(tab)

    def CloseCurrentFit(self, evt):
        self.fitMultiSwitch.removeCurrentTab()

    def ExitApp(self, evt):
        try:
            service.SettingsProvider.getInstance().saveAll()
            self.Close()
        except PyDeadObjectError:
            pass

    def ShowAboutBox(self, evt):
        info = wx.AboutDialogInfo()
        info.Name = "pyfa"
        info.Version = aboutData.versionString
        info.Description = wordwrap(aboutData.description + "\n\n\nDevelopers: " + ", ".join(aboutData.developers) + "\n\nAdditional credits:\n" + "\n".join(aboutData.credits) + "\n\nLicense: " + aboutData.license + " - see included " + aboutData.licenseLocation,
            550, wx.ClientDC(self))
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
        self.Bind(wx.EVT_MENU, self.showPreferenceDialog, id=wx.ID_PREFERENCES)

        #Clipboard exports
        self.Bind(wx.EVT_MENU, self.exportToClipboard, id=wx.ID_COPY)

        #Graphs
        self.Bind(wx.EVT_MENU, self.openGraphFrame, id=menuBar.graphFrameId)

        toggleShipMarketId = wx.NewId()
        # Close Tab
        self.Bind(wx.EVT_MENU, self.CloseCurrentFit, id=self.closeTabId)
        self.Bind(wx.EVT_MENU,self.HAddTab, id = self.addTabId)
        self.Bind(wx.EVT_MENU,self.toggleShipMarket, id = toggleShipMarketId)

        actb = [(wx.ACCEL_CTRL, ord('T'), self.addTabId),
                (wx.ACCEL_CMD, ord('T'), self.addTabId),
                (wx.ACCEL_CTRL, ord("W"), self.closeTabId),
                (wx.ACCEL_CMD, ord("W"), self.closeTabId),
                (wx.ACCEL_CTRL, ord(" "), toggleShipMarketId),
                (wx.ACCEL_CMD, ord(" "), toggleShipMarketId)]
        atable = wx.AcceleratorTable(actb)
        self.SetAcceleratorTable(atable)


    def HAddTab(self,event):
        self.fitMultiSwitch.AddTab()

    def toggleShipMarket(self, event):
        sel = self.notebookBrowsers.GetSelection()
        self.notebookBrowsers.SetSelection(0 if sel == 1 else 1)

    def clipboardEft(self):
        sFit = service.Fit.getInstance()
        self.toClipboard(sFit.exportFit(self.getActiveFit()))

    def clipboardDna(self):
        sFit = service.Fit.getInstance()
        self.toClipboard(sFit.exportDna(self.getActiveFit()))

    def clipboardXml(self):
        sFit = service.Fit.getInstance()
        self.toClipboard(sFit.exportXml(self.getActiveFit()))

    def importFromClipboard(self, event):
        sFit = service.Fit.getInstance()
        try:
            fits = sFit.importFitFromBuffer(self.fromClipboard())
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

    def toClipboard(self, text):
        clip = wx.TheClipboard
        clip.Open()
        data = wx.TextDataObject(text)
        clip.SetData(data)
        clip.Close()

    def fromClipboard(self):
        clip = wx.TheClipboard
        clip.Open()
        data = wx.TextDataObject("")
        if clip.GetData(data):
            clip.Close()
            return data.GetText()
        else:
            clip.Close()
            return None

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
        if self.waitDialog.timer.IsRunning():
            self.waitDialog.timer.Stop()
        self.waitDialog.Destroy()

    def openGraphFrame(self, event):
        graphFrame = GraphFrame(self)
        graphFrame.Show()

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
        wx.Dialog.__init__ (self, parent, id=wx.ID_ANY, title=u"Please wait ...", size=(200,30),
                           style=wx.NO_BORDER)
        mainSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.progress = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL | wx.GA_SMOOTH )
        mainSizer.Add( self.progress, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )
        self.progress.SetRange(20)
        self.progress.SetValue(0)
        self.cycle = 0
        self.SetSizer( mainSizer )
        self.Layout()
        self.timer = wx.Timer(self,wx.ID_ANY)
        self.timer.Start(100)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.Bind(wx.EVT_TIMER,self.OnTimer)
        self.CenterOnParent()

    def OnTimer(self, event):
        self.cycle += 1
        if self.cycle > self.progress.GetRange():
            self.cycle = 0
        self.progress.SetValue(self.cycle)

    def OnClose(self, event):
        pass
