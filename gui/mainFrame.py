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
import time

from wx._core import PyDeadObjectError
from wx.lib.wordwrap import wordwrap

import service
import config
import threading

import gui.aboutData
import gui.chromeTabs
import gui.utils.animUtils as animUtils
import gui.globalEvents as GE

from gui.bitmapLoader import BitmapLoader
from gui.mainMenuBar import MainMenuBar
from gui.additionsPane import AdditionsPane
from gui.marketBrowser import MarketBrowser, ItemSelected
from gui.multiSwitch import MultiSwitch
from gui.statsPane import StatsPane
from gui.shipBrowser import ShipBrowser, FitSelected, ImportSelected, Stage3Selected
from gui.characterEditor import CharacterEditor, SaveCharacterAs
from gui.crestFittings import CrestFittings
from gui.characterSelection import CharacterSelection
from gui.patternEditor import DmgPatternEditorDlg
from gui.resistsEditor import ResistsEditorDlg
from gui.preferenceDialog import PreferenceDialog
from gui.graphFrame import GraphFrame
from gui.copySelectDialog import CopySelectDialog
from gui.utils.clipboard import toClipboard, fromClipboard
from gui.fleetBrowser import FleetBrowser
from gui.updateDialog import UpdateDialog
from gui.builtinViews import *

from time import gmtime, strftime

#dummy panel(no paint no erasebk)
class PFPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnBkErase)

    def OnPaint(self, event):
        event.Skip()
    def OnBkErase(self, event):
        pass

class OpenFitsThread(threading.Thread):
    def __init__(self, fits, callback):
        threading.Thread.__init__(self)
        self.mainFrame = MainFrame.getInstance()
        self.callback = callback
        self.fits = fits
        self.start()

    def run(self):
        time.sleep(0.5)  # Give GUI some time to finish drawing

        # `startup` tells FitSpawner that we are loading fits are startup, and
        # has 3 values:
        # False = Set as default in FitSpawner itself, never set here
        # 1 = Create new fit page, but do not calculate page
        # 2 = Create new page and calculate
        # We use 1 for all fits except the last one where we use 2 so that we
        # have correct calculations displayed at startup
        for fitID in self.fits[:-1]:
            wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID, startup=1))

        wx.PostEvent(self.mainFrame, FitSelected(fitID=self.fits[-1], startup=2))
        wx.CallAfter(self.callback)

class MainFrame(wx.Frame):
    __instance = None
    @classmethod
    def getInstance(cls):
        return cls.__instance if cls.__instance is not None else MainFrame()

    def __init__(self):
        title="pyfa %s%s - Python Fitting Assistant"%(config.version, "" if config.tag.lower() != 'git' else " (git)")
        wx.Frame.__init__(self, None, wx.ID_ANY, title)

        MainFrame.__instance = self

        #Load stored settings (width/height/maximized..)
        self.LoadMainFrameAttribs()

        #Fix for msw (have the frame background color match panel color
        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        #Load and set the icon for pyfa main window
        i = wx.IconFromBitmap(BitmapLoader.getBitmap("pyfa", "gui"))
        self.SetIcon(i)

        #Create the layout and windows
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.browser_fitting_split = wx.SplitterWindow(self, style = wx.SP_LIVE_UPDATE)
        self.fitting_additions_split = wx.SplitterWindow(self.browser_fitting_split, style = wx.SP_LIVE_UPDATE)

        mainSizer.Add(self.browser_fitting_split, 1, wx.EXPAND | wx.LEFT, 2)

        self.fitMultiSwitch = MultiSwitch(self.fitting_additions_split)
        self.additionsPane = AdditionsPane(self.fitting_additions_split)

        self.notebookBrowsers = gui.chromeTabs.PFNotebook(self.browser_fitting_split, False)

        marketImg = BitmapLoader.getImage("market_small", "gui")
        shipBrowserImg = BitmapLoader.getImage("ship_small", "gui")

        self.marketBrowser = MarketBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.marketBrowser, "Market", tabImage = marketImg, showClose = False)
        self.marketBrowser.splitter.SetSashPosition(self.marketHeight)

        self.shipBrowser = ShipBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.shipBrowser, "Ships", tabImage = shipBrowserImg, showClose = False)

        #=======================================================================
        # DISABLED FOR RC2 RELEASE
        #self.fleetBrowser = FleetBrowser(self.notebookBrowsers)
        #self.notebookBrowsers.AddPage(self.fleetBrowser, "Fleets", showClose = False)
        #=======================================================================

        self.notebookBrowsers.SetSelection(1)

        self.browser_fitting_split.SplitVertically(self.notebookBrowsers, self.fitting_additions_split)
        self.browser_fitting_split.SetMinimumPaneSize(204)
        self.browser_fitting_split.SetSashPosition(self.browserWidth)

        self.fitting_additions_split.SplitHorizontally(self.fitMultiSwitch, self.additionsPane, -200)
        self.fitting_additions_split.SetMinimumPaneSize(200)
        self.fitting_additions_split.SetSashPosition(self.fittingHeight)
        self.fitting_additions_split.SetSashGravity(1.0)

        cstatsSizer = wx.BoxSizer(wx.VERTICAL)

        self.charSelection = CharacterSelection(self)
        cstatsSizer.Add(self.charSelection, 0, wx.EXPAND)

        self.statsPane = StatsPane(self)
        cstatsSizer.Add(self.statsPane, 0, wx.EXPAND)

        mainSizer.Add(cstatsSizer, 0, wx.EXPAND)

        self.SetSizer(mainSizer)

        #Add menu
        self.addPageId = wx.NewId()
        self.closePageId = wx.NewId()

        self.widgetInspectMenuID = wx.NewId()
        self.SetMenuBar(MainMenuBar())
        self.registerMenu()

        #Internal vars to keep track of other windows (graphing/stats)
        self.graphFrame = None
        self.statsWnds = []
        self.activeStatsWnd = None

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        #Show ourselves
        self.Show()

        self.LoadPreviousOpenFits()

        #Check for updates
        self.sUpdate = service.Update.getInstance()
        self.sUpdate.CheckUpdate(self.ShowUpdateBox)

    def ShowUpdateBox(self, release):
        dlg = UpdateDialog(self, release)
        dlg.ShowModal()

    def LoadPreviousOpenFits(self):
        sFit = service.Fit.getInstance()

        self.prevOpenFits = service.SettingsProvider.getInstance().getSettings("pyfaPrevOpenFits", {"enabled": False, "pyfaOpenFits": []})
        fits = self.prevOpenFits['pyfaOpenFits']

        # Remove any fits that cause exception when fetching (non-existent fits)
        for id in fits[:]:
            try:
                sFit.getFit(id, basic=True)
            except:
                fits.remove(id)

        if not self.prevOpenFits['enabled'] or len(fits) is 0:
            # add blank page if there are no fits to be loaded
            self.fitMultiSwitch.AddPage()
            return

        self.waitDialog = wx.BusyInfo("Loading previous fits...")
        OpenFitsThread(fits, self.closeWaitDialog)

    def LoadMainFrameAttribs(self):
        mainFrameDefaultAttribs = {"wnd_width": 1000, "wnd_height": 700, "wnd_maximized": False, "browser_width": 300, "market_height": 0, "fitting_height": -200}
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

        self.browserWidth = self.mainFrameAttribs["browser_width"]
        self.marketHeight = self.mainFrameAttribs["market_height"]
        self.fittingHeight = self.mainFrameAttribs["fitting_height"]

    def UpdateMainFrameAttribs(self):
        if self.IsIconized():
            return
        width,height = self.GetSize()

        self.mainFrameAttribs["wnd_width"] = width
        self.mainFrameAttribs["wnd_height"] = height
        self.mainFrameAttribs["wnd_maximized"] = self.IsMaximized()

        self.mainFrameAttribs["browser_width"] = self.notebookBrowsers.GetSize()[0]
        self.mainFrameAttribs["market_height"] = self.marketBrowser.marketView.GetSize()[1]
        self.mainFrameAttribs["fitting_height"] = self.fitting_additions_split.GetSashPosition()

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

        # save open fits
        self.prevOpenFits['pyfaOpenFits'] = [] # clear old list
        for page in self.fitMultiSwitch.pages:
            m = getattr(page, "getActiveFit", None)
            if m is not None:
                 self.prevOpenFits['pyfaOpenFits'].append(m())

        # save all teh settingz
        service.SettingsProvider.getInstance().saveAll()
        event.Skip()

    def ExitApp(self, event):
        self.Close()
        event.Skip()

    def ShowAboutBox(self, evt):
        import eos.config
        info = wx.AboutDialogInfo()
        info.Name = "pyfa"
        info.Version = gui.aboutData.versionString
        info.Description = wordwrap(gui.aboutData.description + "\n\nDevelopers:\n\t" +
                                     "\n\t".join(gui.aboutData.developers) +
                                     "\n\nAdditional credits:\n\t" +
                                     "\n\t".join(gui.aboutData.credits) +
                                     "\n\nLicenses:\n\t" +
                                     "\n\t".join(gui.aboutData.licenses) +
                                     "\n\nEVE Data: \t" + eos.config.gamedata_version +
                                     "\nPython: \t" + sys.version +
                                     "\nwxPython: \t" + wx.__version__ +
                                     "\nSQLAlchemy: \t" + sqlalchemy.__version__,
            700, wx.ClientDC(self))
        if "__WXGTK__" in  wx.PlatformInfo:
            forumUrl = "http://forums.eveonline.com/default.aspx?g=posts&amp;t=247609"
        else:
            forumUrl = "http://forums.eveonline.com/default.aspx?g=posts&t=247609"
        info.WebSite = (forumUrl, "pyfa thread at EVE Online forum")
        wx.AboutBox(info)


    def showCharacterEditor(self, event):
        dlg=CharacterEditor(self)
        dlg.Show()

    def showTargetResistsEditor(self, event):
        dlg=ResistsEditorDlg(self)
        dlg.ShowModal()
        dlg.Destroy()

    def showDamagePatternEditor(self, event):
        dlg=DmgPatternEditorDlg(self)
        dlg.ShowModal()
        dlg.Destroy()

    def showExportDialog(self, event):
        """ Export active fit """
        sFit = service.Fit.getInstance()
        fit = sFit.getFit(self.getActiveFit())
        defaultFile = "%s - %s.xml"%(fit.ship.item.name, fit.name) if fit else None

        dlg = wx.FileDialog(self, "Save Fitting As...",
                            wildcard = "EVE XML fitting files (*.xml)|*.xml",
                            style = wx.FD_SAVE,
                            defaultFile=defaultFile)
        if dlg.ShowModal() == wx.ID_OK:
            format = dlg.GetFilterIndex()
            path = dlg.GetPath()
            if format == 0:
                output = sFit.exportXml(None, self.getActiveFit())
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

    def goWiki(self, event):
        wx.LaunchDefaultBrowser('https://github.com/DarkFenX/Pyfa/wiki')

    def goForums(self, event):
        wx.LaunchDefaultBrowser('https://forums.eveonline.com/default.aspx?g=posts&t=247609')

    def registerMenu(self):
        menuBar = self.GetMenuBar()
        # Quit
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        # Widgets Inspector
        if config.debug:
            self.Bind(wx.EVT_MENU, self.openWXInspectTool, id = self.widgetInspectMenuID)
        # About
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)
        # Char editor
        self.Bind(wx.EVT_MENU, self.showCharacterEditor, id=menuBar.characterEditorId)
        # Damage pattern editor
        self.Bind(wx.EVT_MENU, self.showDamagePatternEditor, id=menuBar.damagePatternEditorId)
        # Target Resists editor
        self.Bind(wx.EVT_MENU, self.showTargetResistsEditor, id=menuBar.targetResistsEditorId)
        # Import dialog
        self.Bind(wx.EVT_MENU, self.fileImportDialog, id=wx.ID_OPEN)
        # Export dialog
        self.Bind(wx.EVT_MENU, self.showExportDialog, id=wx.ID_SAVEAS)
        # Import from Clipboard
        self.Bind(wx.EVT_MENU, self.importFromClipboard, id=wx.ID_PASTE)
        # Backup fits
        self.Bind(wx.EVT_MENU, self.backupToXml, id=menuBar.backupFitsId)
        # Export skills needed
        self.Bind(wx.EVT_MENU, self.exportSkillsNeeded, id=menuBar.exportSkillsNeededId)
        # Import character
        self.Bind(wx.EVT_MENU, self.importCharacter, id=menuBar.importCharacterId)
        # Export HTML
        self.Bind(wx.EVT_MENU, self.exportHtml, id=menuBar.exportHtmlId)
        # Preference dialog
        self.Bind(wx.EVT_MENU, self.showPreferenceDialog, id=wx.ID_PREFERENCES)
        # User guide
        self.Bind(wx.EVT_MENU, self.goWiki, id = menuBar.wikiId)
        # EVE Forums
        self.Bind(wx.EVT_MENU, self.goForums, id = menuBar.forumId)
        # Save current character
        self.Bind(wx.EVT_MENU, self.saveChar, id = menuBar.saveCharId)
        # Save current character as another character
        self.Bind(wx.EVT_MENU, self.saveCharAs, id = menuBar.saveCharAsId)
        # Save current character
        self.Bind(wx.EVT_MENU, self.revertChar, id = menuBar.revertCharId)
        # Browse fittings
        self.Bind(wx.EVT_MENU, self.eveFittings, id = menuBar.eveFittingsId)

        #Clipboard exports
        self.Bind(wx.EVT_MENU, self.exportToClipboard, id=wx.ID_COPY)

        #Graphs
        self.Bind(wx.EVT_MENU, self.openGraphFrame, id=menuBar.graphFrameId)

        toggleSearchBoxId = wx.NewId()
        toggleShipMarketId = wx.NewId()
        ctabnext = wx.NewId()
        ctabprev = wx.NewId()

        # Close Page
        self.Bind(wx.EVT_MENU, self.CloseCurrentPage, id=self.closePageId)
        self.Bind(wx.EVT_MENU, self.HAddPage, id = self.addPageId)
        self.Bind(wx.EVT_MENU, self.toggleSearchBox, id = toggleSearchBoxId)
        self.Bind(wx.EVT_MENU, self.toggleShipMarket, id = toggleShipMarketId)
        self.Bind(wx.EVT_MENU, self.CTabNext, id = ctabnext)
        self.Bind(wx.EVT_MENU, self.CTabPrev, id = ctabprev)

        actb = [(wx.ACCEL_CTRL, ord('T'), self.addPageId),
                (wx.ACCEL_CMD, ord('T'), self.addPageId),

                (wx.ACCEL_CTRL, ord('F'), toggleSearchBoxId),
                (wx.ACCEL_CMD, ord('F'), toggleSearchBoxId),

                (wx.ACCEL_CTRL, ord("W"), self.closePageId),
                (wx.ACCEL_CTRL, wx.WXK_F4, self.closePageId),
                (wx.ACCEL_CMD, ord("W"), self.closePageId),

                (wx.ACCEL_CTRL, ord(" "), toggleShipMarketId),
                (wx.ACCEL_CMD, ord(" "), toggleShipMarketId),

                # Ctrl+(Shift+)Tab
                (wx.ACCEL_CTRL, wx.WXK_TAB, ctabnext),
                (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, wx.WXK_TAB, ctabprev),
                (wx.ACCEL_CMD, wx.WXK_TAB, ctabnext),
                (wx.ACCEL_CMD | wx.ACCEL_SHIFT, wx.WXK_TAB, ctabprev),

                # Ctrl+Page(Up/Down)
                (wx.ACCEL_CTRL, wx.WXK_PAGEDOWN, ctabnext),
                (wx.ACCEL_CTRL, wx.WXK_PAGEUP, ctabprev),
                (wx.ACCEL_CMD, wx.WXK_PAGEDOWN, ctabnext),
                (wx.ACCEL_CMD, wx.WXK_PAGEUP, ctabprev)
                ]

        # Ctrl/Cmd+# for addition pane selection
        self.additionsSelect = []
        for i in range(0, self.additionsPane.notebook.GetPageCount()):
            self.additionsSelect.append(wx.NewId())
            self.Bind(wx.EVT_MENU, self.AdditionsTabSelect, id=self.additionsSelect[i])
            actb.append((wx.ACCEL_CMD, i+49, self.additionsSelect[i]))
            actb.append((wx.ACCEL_CTRL, i+49, self.additionsSelect[i]))

        # Alt+1-9 for market item selection
        self.itemSelect = []
        for i in range(0, 9):
            self.itemSelect.append(wx.NewId())
            self.Bind(wx.EVT_MENU, self.ItemSelect, id = self.itemSelect[i])
            actb.append((wx.ACCEL_ALT, i + 49, self.itemSelect[i]))

        atable = wx.AcceleratorTable(actb)
        self.SetAcceleratorTable(atable)

    def eveFittings(self, event):
        dlg=CrestFittings(self)
        dlg.Show()

    def saveChar(self, event):
        sChr = service.Character.getInstance()
        charID = self.charSelection.getActiveCharacter()
        sChr.saveCharacter(charID)
        wx.PostEvent(self, GE.CharListUpdated())

    def saveCharAs(self, event):
        charID = self.charSelection.getActiveCharacter()
        dlg = SaveCharacterAs(self, charID)
        dlg.ShowModal()
        dlg.Destroy()

    def revertChar(self, event):
        sChr = service.Character.getInstance()
        charID = self.charSelection.getActiveCharacter()
        sChr.revertCharacter(charID)
        wx.PostEvent(self, GE.CharListUpdated())

    def AdditionsTabSelect(self, event):
        selTab = self.additionsSelect.index(event.GetId())

        if selTab <= self.additionsPane.notebook.GetPageCount():
            self.additionsPane.notebook.SetSelection(selTab)

    def ItemSelect(self, event):
        selItem = self.itemSelect.index(event.GetId())

        if selItem < len(self.marketBrowser.itemView.active):
            wx.PostEvent(self, ItemSelected(itemID=self.marketBrowser.itemView.active[selItem].ID))

    def CTabNext(self, event):
        self.fitMultiSwitch.NextPage()

    def CTabPrev(self, event):
        self.fitMultiSwitch.PrevPage()

    def HAddPage(self,event):
        self.fitMultiSwitch.AddPage()

    def toggleShipMarket(self, event):
        sel = self.notebookBrowsers.GetSelection()
        self.notebookBrowsers.SetSelection(0 if sel == 1 else 1)

    def toggleSearchBox(self, event):
        sel = self.notebookBrowsers.GetSelection()
        if sel == 1:
            self.shipBrowser.navpanel.ToggleSearchBox()
        else:
            self.marketBrowser.search.Focus()

    def clipboardEft(self):
        sFit = service.Fit.getInstance()
        toClipboard(sFit.exportFit(self.getActiveFit()))

    def clipboardEftImps(self):
        sFit = service.Fit.getInstance()
        toClipboard(sFit.exportEftImps(self.getActiveFit()))

    def clipboardDna(self):
        sFit = service.Fit.getInstance()
        toClipboard(sFit.exportDna(self.getActiveFit()))

    def clipboardXml(self):
        sFit = service.Fit.getInstance()
        toClipboard(sFit.exportXml(None, self.getActiveFit()))

    def importFromClipboard(self, event):
        sFit = service.Fit.getInstance()
        try:
            fits = sFit.importFitFromBuffer(fromClipboard(), self.getActiveFit())
        except:
            pass
        else:
            self._openAfterImport(fits)

    def exportToClipboard(self, event):
        CopySelectDict = {CopySelectDialog.copyFormatEft: self.clipboardEft,
                          CopySelectDialog.copyFormatEftImps: self.clipboardEftImps,
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

    def exportSkillsNeeded(self, event):
        """ Exports skills needed for active fit and active character """
        sCharacter = service.Character.getInstance()
        saveDialog = wx.FileDialog(self, "Export Skills Needed As...",
                    wildcard = "EVEMon skills training file (*.emp)|*.emp|" \
                               "EVEMon skills training XML file (*.xml)|*.xml|" \
                               "Text skills training file (*.txt)|*.txt",
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveDialog.ShowModal() == wx.ID_OK:
            saveFmtInt = saveDialog.GetFilterIndex()

            if saveFmtInt == 0:  # Per ordering of wildcards above
                saveFmt = "emp"
            elif saveFmtInt == 1:
                saveFmt = "xml"
            else:
                saveFmt = "txt"

            filePath = saveDialog.GetPath()
            if '.' not in os.path.basename(filePath):
                filePath += ".{0}".format(saveFmt)

            self.waitDialog = wx.BusyInfo("Exporting skills needed...")
            sCharacter.backupSkills(filePath, saveFmt, self.getActiveFit(), self.closeWaitDialog)

        saveDialog.Destroy()

    def fileImportDialog(self, event):
        """Handles importing single/multiple EVE XML / EFT cfg fit files"""
        sFit = service.Fit.getInstance()
        dlg = wx.FileDialog(self, "Open One Or More Fitting Files",
                    wildcard = "EVE XML fitting files (*.xml)|*.xml|" \
                                "EFT text fitting files (*.cfg)|*.cfg|" \
                                "All Files (*)|*",
                    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if (dlg.ShowModal() == wx.ID_OK):
            self.progressDialog = wx.ProgressDialog(
                            "Importing fits",
                            " "*100, # set some arbitrary spacing to create width in window
                            parent=self, style = wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)
            self.progressDialog.message = None
            sFit.importFitsThreaded(dlg.GetPaths(), self.fileImportCallback)
            self.progressDialog.ShowModal()
            dlg.Destroy()

    def backupToXml(self, event):
        """ Back up all fits to EVE XML file """
        defaultFile = "pyfa-fits-%s.xml"%strftime("%Y%m%d_%H%M%S", gmtime())

        saveDialog = wx.FileDialog(self, "Save Backup As...",
                            wildcard = "EVE XML fitting file (*.xml)|*.xml",
                            style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                            defaultFile=defaultFile)

        if saveDialog.ShowModal() == wx.ID_OK:
            filePath = saveDialog.GetPath()
            if '.' not in os.path.basename(filePath):
                filePath += ".xml"

            sFit = service.Fit.getInstance()
            max = sFit.countAllFits()

            self.progressDialog = wx.ProgressDialog("Backup fits",
                              "Backing up %d fits to: %s"%(max, filePath),
                              maximum=max, parent=self,
                              style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)
            sFit.backupFits(filePath, self.backupCallback)
            self.progressDialog.ShowModal()

    def exportHtml(self, event):
        from gui.utils.exportHtml import exportHtml
        sFit = service.Fit.getInstance()
        settings = service.settings.HTMLExportSettings.getInstance()

        max = sFit.countAllFits()
        path = settings.getPath()

        if not os.path.isdir(os.path.dirname(path)):
            dlg = wx.MessageDialog(self,
                 "Invalid Path\n\nThe following path is invalid or does not exist: \n%s\n\nPlease verify path location pyfa's preferences."%path,
                 "Error", wx.OK | wx.ICON_ERROR)

            if dlg.ShowModal() == wx.ID_OK:
                return

        self.progressDialog = wx.ProgressDialog("Backup fits",
                            "Generating HTML file at: %s"%path,
                            maximum=max, parent=self,
                            style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)

        exportHtml.getInstance().refreshFittingHtml(True, self.backupCallback)
        self.progressDialog.ShowModal()

    def backupCallback(self, info):
        if info == -1:
            self.closeProgressDialog()
        else:
            self.progressDialog.Update(info)

    def fileImportCallback(self, info, fits=None):
        """
        While importing fits from file, the logic calls back to this function to
        update progress bar to show activity. XML files can contain multiple
        ships with multiple fits, whereas EFT cfg files contain many fits of
        a single ship. When iterating through the files, we update the message
        when we start a new file, and then Pulse the progress bar with every fit
        that is processed.
        """

        if info == -1:
            self.closeProgressDialog()
            self._openAfterImport(fits)
        elif info != self.progressDialog.message and info is not None:
            # New message, overwrite cached message and update
            self.progressDialog.message = info
            self.progressDialog.Pulse(info)
        else:
            # Simply Pulse() if we don't have anything else to do
            self.progressDialog.Pulse()

    def _openAfterImport(self, fits):
        if len(fits) > 0:
            if len(fits) == 1:
                fit = fits[0]
                wx.PostEvent(self, FitSelected(fitID=fit.ID))
                wx.PostEvent(self.shipBrowser, Stage3Selected(shipID=fit.shipID, back=True))
            else:
                wx.PostEvent(self.shipBrowser, ImportSelected(fits=fits, back=True))

    def closeProgressDialog(self):
        # Windows apparently handles ProgressDialogs differently. We can
        # simply Destroy it here, but for other platforms we must Close it
        if 'wxMSW' in wx.PlatformInfo:
            self.progressDialog.Destroy()
        else:
            self.progressDialog.EndModal(wx.ID_OK)
            self.progressDialog.Close()

    def importCharacter(self, event):
        """ Imports character XML file from EVE API """
        dlg = wx.FileDialog(self, "Open One Or More Character Files",
                        wildcard="EVE API XML character files (*.xml)|*.xml|" \
                                   "All Files (*)|*",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.waitDialog = wx.BusyInfo("Importing Character...")
            sCharacter = service.Character.getInstance()
            sCharacter.importCharacter(dlg.GetPaths(), self.importCharacterCallback)

    def importCharacterCallback(self):
        self.closeWaitDialog()
        wx.PostEvent(self, GE.CharListUpdated())

    def closeWaitDialog(self):
        del self.waitDialog

    def openGraphFrame(self, event):
        if not self.graphFrame:
            self.graphFrame = GraphFrame(self)
            if gui.graphFrame.enabled:
                self.graphFrame.Show()
        else:
            self.graphFrame.SetFocus()

    def openWXInspectTool(self, event):
        from wx.lib.inspection import InspectionTool
        if not InspectionTool().initialized:
            InspectionTool().Init()

        # Find a widget to be selected in the tree.  Use either the
        # one under the cursor, if any, or this frame.
        wnd = wx.FindWindowAtPointer()
        if not wnd:
            wnd = self
        InspectionTool().Show(wnd, True)

