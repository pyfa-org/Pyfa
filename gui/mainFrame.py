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
from gui.importExport import ImportDialog, ExportDialog
from gui.preferenceDialog import PreferenceDialog
import aboutData
import gui.fittingView as fv
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
        self.notebookBrowsers.SetSelection(1)

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

        self.statsCharPickerSizer = wx.BoxSizer(wx.VERTICAL)
        self.statsSizer.Add(self.statsCharPickerSizer, 0, wx.EXPAND | wx.TOP | wx.RIGHT | wx.LEFT, 3)

        self.charSelection = CharacterSelection(statsFitviewPanel)
        self.statsCharPickerSizer.Add(self.charSelection, 0, wx.EXPAND)

        self.statsPane = StatsPane(statsFitviewPanel)
        self.statsCharPickerSizer.Add(self.statsPane, 0, wx.EXPAND)

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
        info.Description = wordwrap(aboutData.description + "\n\n\nDevelopers: " + ", ".join(aboutData.developers) + "\n\nAdditional credits\n" + "\n".join(aboutData.credits) + "\n\nLicense: " + aboutData.license + " see included " + aboutData.licenseLocation,
            350, wx.ClientDC(self))
        info.WebSite = ("http://pyfa.sourceforge.net/", "pyfa home page")
        wx.AboutBox(info)

    def showCharacterEditor(self, event):
        dlg=CharacterEditor(self)
        dlg.Show()

        cFit = service.Fit.getInstance()
        cFit.clearFit(self.getActiveFit())
        wx.PostEvent(self, fv.FitChanged(fitID=self.getActiveFit()))

    def showDamagePatternEditor(self, event):
        dlg=DmgPatternEditorDlg(self)
        dlg.ShowModal()
        dlg.Destroy()

    def showImportDialog(self, event):
        fits = []
        sFit = service.Fit.getInstance()
        dlg=wx.FileDialog(
            self,
            "Choose one or more fitting files to import",
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

    def showExportDialog(self, event):
        dlg=wx.FileDialog(
            self,
            "Choose a file to export the current fitting to",
            wildcard = "EFT text fitting files (*.cfg)|*.cfg|EvE XML fitting files (*.xml)|*.xml",
            style = wx.FD_SAVE)
        if (dlg.ShowModal() == wx.ID_OK):
            sFit = service.Fit.getInstance()
            format = dlg.GetFilterIndex()
            output = ""
            path = dlg.GetPath()
            if (format == 0):
                output = sFit.exportFit(self.getActiveFit())
                path += ".cfg"
            elif (format == 1):
                output = sFit.exportXml(self.getActiveFit())
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
        # Close Tab
        self.Bind(wx.EVT_MENU, self.CloseCurrentFit, id=wx.ID_CLOSE)
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
        self.Bind(wx.EVT_MENU, self.clipboardEft, id=menuBar.idExportEft)
        self.Bind(wx.EVT_MENU, self.clipboardDna, id=menuBar.idExportDna)
        self.Bind(wx.EVT_MENU, self.clipboardXml, id=menuBar.idExportXml)

    def clipboardEft(self, event):
        sFit = service.Fit.getInstance()
        self.toClipboard(sFit.exportFit(self.getActiveFit()))

    def clipboardDna(self, event):
        sFit = service.Fit.getInstance()
        self.toClipboard(sFit.exportDna(self.getActiveFit()))

    def clipboardXml(self, event):
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
            "Choose where to save the backup",
            wildcard = "EvE XML fitting file (*.xml)|*.xml",
            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if (saveDialog.ShowModal() == wx.ID_OK):
            filePath = saveDialog.GetPath()
            sFit.backupFits(filePath)
        saveDialog.Destroy()

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

