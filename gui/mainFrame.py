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

import sys
import os.path
import logging

import sqlalchemy
import wx
import time

from codecs import open

from wx.lib.wordwrap import wordwrap

import config
from config import parsePath
from gui.graph import Graph

from eos.config import gamedata_version

import gui.aboutData
from gui.chromeTabs import PFNotebook
import gui.globalEvents as GE

from gui.bitmapLoader import BitmapLoader
from gui.additionsPane import AdditionsPane
from gui.marketBrowser import MarketBrowser, ItemSelected
from gui.multiSwitch import MultiSwitch
from gui.statsPane import StatsPane
from gui.shipBrowser import ShipBrowser, FitSelected, ImportSelected, Stage3Selected, FitList
from gui.characterEditor import CharacterEditor, SaveCharacterAs
from gui.characterSelection import CharacterSelection
from gui.patternEditor import DmgPatternEditorDlg
from gui.resistsEditor import ResistsEditorDlg
from gui.setEditor import ImplantSetEditorDlg
from gui.preferenceDialog import PreferenceDialog
from gui.copySelectDialog import CopySelectDialog
from gui.utils.clipboard import toClipboard, fromClipboard
from gui.updateDialog import UpdateDialog
from gui.builtinViews import fittingView, implantEditor

from service.settings import SettingsProvider
from service.fit import Fit
from service.character import Character
from service.update import Update

# import this to access override setting
from eos.modifiedAttributeDict import ModifiedAttributeDict
from eos.db.saveddata.loadDefaultDatabaseValues import DefaultDatabaseValues
from eos import db
from service.port import Port
from service.settings import HTMLExportSettings

from time import gmtime, strftime

import threading
import webbrowser

try:
    import matplotlib as mpl
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as Canvas
    from matplotlib.figure import Figure
    graphFrame_enabled = True
    mplImported = False
except ImportError:
    mpl = None
    Canvas = None
    Figure = None
    graphFrame_enabled = False

if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
    from service.crest import Crest
    from service.crest import CrestModes
    from gui.crestFittings import CrestFittings, ExportToEve, CrestMgmt

    try:
        from gui.propertyEditor import AttributeEditor

        disableOverrideEditor = False
    except ImportError as e:
        AttributeEditor = None
        print("Error loading Attribute Editor: %s.\nAccess to Attribute Editor is disabled." % e.message)
        disableOverrideEditor = True

logger = logging.getLogger("pyfa.gui.mainFrame")

if not graphFrame_enabled:
    logger.info("Problems importing matplotlib; continuing without graphs")


# dummy panel(no paint no erasebk)
class PFPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnBkErase)

    def OnPaint(self, event):
        event.Skip()

    def OnBkErase(self, event):
        pass


class OpenFitsThread(threading.Thread):
    def __init__(self, fits, callback):
        threading.Thread.__init__(self)
        self.name = "LoadingOpenFits"
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

    def __init__(self, title):
        self.title = title
        wx.Frame.__init__(self, None, wx.ID_ANY, self.title)

        MainFrame.__instance = self

        # Load stored settings (width/height/maximized..)
        self.LoadMainFrameAttribs()

        # Fix for msw (have the frame background color match panel color
        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        # Load and set the icon for pyfa main window
        i = wx.IconFromBitmap(BitmapLoader.getBitmap("pyfa", "gui"))
        self.SetIcon(i)

        # Create the layout and windows
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.browser_fitting_split = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.fitting_additions_split = wx.SplitterWindow(self.browser_fitting_split, style=wx.SP_LIVE_UPDATE)

        mainSizer.Add(self.browser_fitting_split, 1, wx.EXPAND | wx.LEFT, 2)

        self.fitMultiSwitch = MultiSwitch(self.fitting_additions_split)
        self.additionsPane = AdditionsPane(self.fitting_additions_split)

        self.notebookBrowsers = PFNotebook(self.browser_fitting_split, False)

        marketImg = BitmapLoader.getImage("market_small", "gui")
        shipBrowserImg = BitmapLoader.getImage("ship_small", "gui")

        self.marketBrowser = MarketBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.marketBrowser, "Market", tabImage=marketImg, showClose=False)
        self.marketBrowser.splitter.SetSashPosition(self.marketHeight)

        self.shipBrowser = ShipBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.shipBrowser, "Fittings", tabImage=shipBrowserImg, showClose=False)

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

        # Add menu
        self.addPageId = wx.NewId()
        self.closePageId = wx.NewId()

        self.widgetInspectMenuID = wx.NewId()
        self.SetMenuBar(MainMenuBar())
        self.registerMenu()

        # Internal vars to keep track of other windows (graphing/stats)
        self.graphFrame = None
        self.statsWnds = []
        self.activeStatsWnd = None

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show ourselves
        self.Show()

        self.LoadPreviousOpenFits()

        # Check for updates
        self.sUpdate = Update.getInstance()
        self.sUpdate.CheckUpdate(self.ShowUpdateBox)

        if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
            self.Bind(GE.EVT_SSO_LOGIN, self.onSSOLogin)
            self.Bind(GE.EVT_SSO_LOGOUT, self.onSSOLogout)

        self.titleTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateTitle, self.titleTimer)

    def ShowUpdateBox(self, release):
        dlg = UpdateDialog(self, release)
        dlg.ShowModal()

    def LoadPreviousOpenFits(self):
        sFit = Fit.getInstance()

        self.prevOpenFits = SettingsProvider.getInstance().getSettings("pyfaPrevOpenFits",
                                                                       {"enabled": False, "pyfaOpenFits": []})
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
        mainFrameDefaultAttribs = {"wnd_width": 1000, "wnd_height": 700, "wnd_maximized": False, "browser_width": 300,
                                   "market_height": 0, "fitting_height": -200}
        self.mainFrameAttribs = SettingsProvider.getInstance().getSettings("pyfaMainWindowAttribs",
                                                                           mainFrameDefaultAttribs)

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
        width, height = self.GetSize()

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
        self.fitMultiSwitch.GetSelectedPage()

    def CloseCurrentPage(self, evt):
        ms = self.fitMultiSwitch

        page = ms.GetSelection()
        if page is not None:
            ms.DeletePage(page)

    def OnClose(self, event):
        self.UpdateMainFrameAttribs()

        # save open fits
        self.prevOpenFits['pyfaOpenFits'] = []  # clear old list
        for page in self.fitMultiSwitch.pages:
            m = getattr(page, "getActiveFit", None)
            if m is not None:
                self.prevOpenFits['pyfaOpenFits'].append(m())

        # save all teh settingz
        SettingsProvider.getInstance().saveAll()
        event.Skip()

    def ExitApp(self, event):
        self.Close()
        event.Skip()

    def ShowAboutBox(self, evt):
        v = sys.version_info
        info = wx.AboutDialogInfo()
        info.Name = "pyfa"
        info.Version = gui.aboutData.versionString
        info.Description = wordwrap(gui.aboutData.description + "\n\nDevelopers:\n\t" +
                                    "\n\t".join(gui.aboutData.developers) +
                                    "\n\nAdditional credits:\n\t" +
                                    "\n\t".join(gui.aboutData.credits) +
                                    "\n\nLicenses:\n\t" +
                                    "\n\t".join(gui.aboutData.licenses) +
                                    "\n\nEVE Data: \t" + gamedata_version +
                                    "\nPython: \t\t" + '{}.{}.{}'.format(v.major, v.minor, v.micro) +
                                    "\nwxPython: \t" + wx.__version__ +
                                    "\nSQLAlchemy: \t" + sqlalchemy.__version__,
                                    500, wx.ClientDC(self))
        if "__WXGTK__" in wx.PlatformInfo:
            forumUrl = "http://forums.eveonline.com/default.aspx?g=posts&amp;t=466425"
        else:
            forumUrl = "http://forums.eveonline.com/default.aspx?g=posts&t=466425"
        info.WebSite = (forumUrl, "pyfa thread at EVE Online forum")
        wx.AboutBox(info)

    def showCharacterEditor(self, event):
        dlg = CharacterEditor(self)
        dlg.Show()

    def showAttrEditor(self, event):
        dlg = AttributeEditor(self)
        dlg.Show()

    def showTargetResistsEditor(self, event):
        ResistsEditorDlg(self)

    def showDamagePatternEditor(self, event):
        dlg = DmgPatternEditorDlg(self)
        dlg.ShowModal()
        dlg.Destroy()

    def showImplantSetEditor(self, event):
        ImplantSetEditorDlg(self)

    def showExportDialog(self, event):
        """ Export active fit """
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.getActiveFit())
        defaultFile = "%s - %s.xml" % (fit.ship.item.name, fit.name) if fit else None

        dlg = wx.FileDialog(self, "Save Fitting As...",
                            wildcard="EVE XML fitting files (*.xml)|*.xml",
                            style=wx.FD_SAVE,
                            defaultFile=defaultFile)
        if dlg.ShowModal() == wx.ID_OK:
            format_ = dlg.GetFilterIndex()
            path = dlg.GetPath()
            if format_ == 0:
                sPort = Port.getInstance()
                output = sPort.exportXml(None, fit)
                if '.' not in os.path.basename(path):
                    path += ".xml"
            else:
                print("oops, invalid fit format %d" % format_)
                dlg.Destroy()
                return

            with open(path, "w", encoding="utf-8") as openfile:
                openfile.write(output)
                openfile.close()

        dlg.Destroy()

    def showPreferenceDialog(self, event):
        dlg = PreferenceDialog(self)
        dlg.ShowModal()

    def goWiki(self, event):
        webbrowser.open('https://github.com/pyfa-org/Pyfa/wiki')

    def goForums(self, event):
        webbrowser.open('https://forums.eveonline.com/default.aspx?g=posts&t=466425')

    def loadDatabaseDefaults(self, event):
        # Import values that must exist otherwise Pyfa breaks
        DefaultDatabaseValues.importRequiredDefaults()
        # Import default values for damage profiles
        DefaultDatabaseValues.importDamageProfileDefaults()
        # Import default values for target resist profiles
        DefaultDatabaseValues.importResistProfileDefaults()

    def registerMenu(self):
        menuBar = self.GetMenuBar()
        # Quit
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        # Load Default Database values
        self.Bind(wx.EVT_MENU, self.loadDatabaseDefaults, id=menuBar.importDatabaseDefaultsId)
        # Widgets Inspector
        if config.debug:
            self.Bind(wx.EVT_MENU, self.openWXInspectTool, id=self.widgetInspectMenuID)
        # About
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)
        # Char editor
        self.Bind(wx.EVT_MENU, self.showCharacterEditor, id=menuBar.characterEditorId)
        # Damage pattern editor
        self.Bind(wx.EVT_MENU, self.showDamagePatternEditor, id=menuBar.damagePatternEditorId)
        # Target Resists editor
        self.Bind(wx.EVT_MENU, self.showTargetResistsEditor, id=menuBar.targetResistsEditorId)
        # Implant Set editor
        self.Bind(wx.EVT_MENU, self.showImplantSetEditor, id=menuBar.implantSetEditorId)
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
        self.Bind(wx.EVT_MENU, self.goWiki, id=menuBar.wikiId)
        # EVE Forums
        self.Bind(wx.EVT_MENU, self.goForums, id=menuBar.forumId)
        # Save current character
        self.Bind(wx.EVT_MENU, self.saveChar, id=menuBar.saveCharId)
        # Save current character as another character
        self.Bind(wx.EVT_MENU, self.saveCharAs, id=menuBar.saveCharAsId)
        # Save current character
        self.Bind(wx.EVT_MENU, self.revertChar, id=menuBar.revertCharId)

        # Browse fittings
        self.Bind(wx.EVT_MENU, self.eveFittings, id=menuBar.eveFittingsId)
        # Export to EVE
        self.Bind(wx.EVT_MENU, self.exportToEve, id=menuBar.exportToEveId)
        # Handle SSO event (login/logout/manage characters, depending on mode and current state)
        self.Bind(wx.EVT_MENU, self.ssoHandler, id=menuBar.ssoLoginId)

        # Open attribute editor
        self.Bind(wx.EVT_MENU, self.showAttrEditor, id=menuBar.attrEditorId)
        # Toggle Overrides
        self.Bind(wx.EVT_MENU, self.toggleOverrides, id=menuBar.toggleOverridesId)

        # Clipboard exports
        self.Bind(wx.EVT_MENU, self.exportToClipboard, id=wx.ID_COPY)

        # Graphs
        self.Bind(wx.EVT_MENU, self.openGraphFrame, id=menuBar.graphFrameId)

        toggleSearchBoxId = wx.NewId()
        toggleShipMarketId = wx.NewId()
        ctabnext = wx.NewId()
        ctabprev = wx.NewId()

        # Close Page
        self.Bind(wx.EVT_MENU, self.CloseCurrentPage, id=self.closePageId)
        self.Bind(wx.EVT_MENU, self.HAddPage, id=self.addPageId)
        self.Bind(wx.EVT_MENU, self.toggleSearchBox, id=toggleSearchBoxId)
        self.Bind(wx.EVT_MENU, self.toggleShipMarket, id=toggleShipMarketId)
        self.Bind(wx.EVT_MENU, self.CTabNext, id=ctabnext)
        self.Bind(wx.EVT_MENU, self.CTabPrev, id=ctabprev)

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
            actb.append((wx.ACCEL_CMD, i + 49, self.additionsSelect[i]))
            actb.append((wx.ACCEL_CTRL, i + 49, self.additionsSelect[i]))

        # Alt+1-9 for market item selection
        self.itemSelect = []
        for i in range(0, 9):
            self.itemSelect.append(wx.NewId())
            self.Bind(wx.EVT_MENU, self.ItemSelect, id=self.itemSelect[i])
            actb.append((wx.ACCEL_ALT, i + 49, self.itemSelect[i]))

        atable = wx.AcceleratorTable(actb)
        self.SetAcceleratorTable(atable)

    def eveFittings(self, event):
        dlg = CrestFittings(self)
        dlg.Show()

    def updateTitle(self, event):
        sCrest = Crest.getInstance()
        char = sCrest.implicitCharacter
        if char:
            t = time.gmtime(char.eve.expires - time.time())
            sTime = time.strftime("%H:%M:%S", t if t >= 0 else 0)
            newTitle = "%s | %s - %s" % (self.title, char.name, sTime)
            self.SetTitle(newTitle)

    def onSSOLogin(self, event):
        menu = self.GetMenuBar()
        menu.Enable(menu.eveFittingsId, True)
        menu.Enable(menu.exportToEveId, True)

        if event.type == CrestModes.IMPLICIT:
            menu.SetLabel(menu.ssoLoginId, "Logout Character")
            self.titleTimer.Start(1000)

    def onSSOLogout(self, event):
        self.titleTimer.Stop()
        self.SetTitle(self.title)

        menu = self.GetMenuBar()
        if event.type == CrestModes.IMPLICIT or event.numChars == 0:
            menu.Enable(menu.eveFittingsId, False)
            menu.Enable(menu.exportToEveId, False)

        if event.type == CrestModes.IMPLICIT:
            menu.SetLabel(menu.ssoLoginId, "Login to EVE")

    def updateCrestMenus(self, type):
        # in case we are logged in when switching, change title back
        self.titleTimer.Stop()
        self.SetTitle(self.title)

        menu = self.GetMenuBar()
        sCrest = Crest.getInstance()

        if type == CrestModes.IMPLICIT:
            menu.SetLabel(menu.ssoLoginId, "Login to EVE")
            menu.Enable(menu.eveFittingsId, False)
            menu.Enable(menu.exportToEveId, False)
        else:
            menu.SetLabel(menu.ssoLoginId, "Manage Characters")
            enable = len(sCrest.getCrestCharacters()) == 0
            menu.Enable(menu.eveFittingsId, not enable)
            menu.Enable(menu.exportToEveId, not enable)

    def ssoHandler(self, event):
        sCrest = Crest.getInstance()
        if sCrest.settings.get('mode') == CrestModes.IMPLICIT:
            if sCrest.implicitCharacter is not None:
                sCrest.logout()
            else:
                uri = sCrest.startServer()
                webbrowser.open(uri)
        else:
            dlg = CrestMgmt(self)
            dlg.Show()

    def exportToEve(self, event):
        dlg = ExportToEve(self)
        dlg.Show()

    def toggleOverrides(self, event):
        ModifiedAttributeDict.OVERRIDES = not ModifiedAttributeDict.OVERRIDES
        wx.PostEvent(self, GE.FitChanged(fitID=self.getActiveFit()))
        menu = self.GetMenuBar()
        menu.SetLabel(menu.toggleOverridesId,
                      "Turn Overrides Off" if ModifiedAttributeDict.OVERRIDES else "Turn Overrides On")

    def saveChar(self, event):
        sChr = Character.getInstance()
        charID = self.charSelection.getActiveCharacter()
        sChr.saveCharacter(charID)
        wx.PostEvent(self, GE.CharListUpdated())

    def saveCharAs(self, event):
        charID = self.charSelection.getActiveCharacter()
        dlg = SaveCharacterAs(self, charID)
        dlg.ShowModal()

    def revertChar(self, event):
        sChr = Character.getInstance()
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

    def HAddPage(self, event):
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
        fit = db.getFit(self.getActiveFit())
        toClipboard(Port.exportEft(fit))

    def clipboardEftImps(self):
        fit = db.getFit(self.getActiveFit())
        toClipboard(Port.exportEftImps(fit))

    def clipboardDna(self):
        fit = db.getFit(self.getActiveFit())
        toClipboard(Port.exportDna(fit))

    def clipboardCrest(self):
        fit = db.getFit(self.getActiveFit())
        toClipboard(Port.exportCrest(fit))

    def clipboardXml(self):
        fit = db.getFit(self.getActiveFit())
        toClipboard(Port.exportXml(None, fit))

    def clipboardMultiBuy(self):
        fit = db.getFit(self.getActiveFit())
        toClipboard(Port.exportMultiBuy(fit))

    def importFromClipboard(self, event):
        clipboard = fromClipboard()
        try:
            fits = Port().importFitFromBuffer(clipboard, self.getActiveFit())
        except:
            logger.error("Attempt to import failed:\n%s", clipboard)
        else:
            self._openAfterImport(fits)

    def exportToClipboard(self, event):
        CopySelectDict = {CopySelectDialog.copyFormatEft: self.clipboardEft,
                          CopySelectDialog.copyFormatEftImps: self.clipboardEftImps,
                          CopySelectDialog.copyFormatXml: self.clipboardXml,
                          CopySelectDialog.copyFormatDna: self.clipboardDna,
                          CopySelectDialog.copyFormatCrest: self.clipboardCrest,
                          CopySelectDialog.copyFormatMultiBuy: self.clipboardMultiBuy}
        dlg = CopySelectDialog(self)
        dlg.ShowModal()
        selected = dlg.GetSelected()

        CopySelectDict[selected]()

        dlg.Destroy()

    def exportSkillsNeeded(self, event):
        """ Exports skills needed for active fit and active character """
        sCharacter = Character.getInstance()
        saveDialog = wx.FileDialog(
            self,
            "Export Skills Needed As...",
            wildcard=("EVEMon skills training file (*.emp)|*.emp|"
                      "EVEMon skills training XML file (*.xml)|*.xml|"
                      "Text skills training file (*.txt)|*.txt"),
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        )

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
        sPort = Port.getInstance()
        dlg = wx.FileDialog(
            self,
            "Open One Or More Fitting Files",
            wildcard=("EVE XML fitting files (*.xml)|*.xml|"
                      "EFT text fitting files (*.cfg)|*.cfg|"
                      "All Files (*)|*"),
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        )
        if (dlg.ShowModal() == wx.ID_OK):
            self.progressDialog = wx.ProgressDialog(
                "Importing fits",
                " " * 100,  # set some arbitrary spacing to create width in window
                parent=self,
                style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME
            )
            self.progressDialog.message = None
            sPort.importFitsThreaded(dlg.GetPaths(), self.fileImportCallback)
            self.progressDialog.ShowModal()
            dlg.Destroy()

    def backupToXml(self, event):
        """ Back up all fits to EVE XML file """
        defaultFile = "pyfa-fits-%s.xml" % strftime("%Y%m%d_%H%M%S", gmtime())

        saveDialog = wx.FileDialog(
            self,
            "Save Backup As...",
            wildcard="EVE XML fitting file (*.xml)|*.xml",
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            defaultFile=defaultFile,
        )

        if saveDialog.ShowModal() == wx.ID_OK:
            filePath = saveDialog.GetPath()
            if '.' not in os.path.basename(filePath):
                filePath += ".xml"

            sFit = Fit.getInstance()
            max_ = sFit.countAllFits()

            self.progressDialog = wx.ProgressDialog(
                "Backup fits",
                "Backing up %d fits to: %s" % (max_, filePath),
                maximum=max_,
                parent=self,
                style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME,
            )
            Port().backupFits(filePath, self.backupCallback)
            self.progressDialog.ShowModal()

    def exportHtml(self, event):
        from gui.utils.exportHtml import exportHtml
        sFit = Fit.getInstance()
        settings = HTMLExportSettings.getInstance()

        max_ = sFit.countAllFits()
        path = settings.getPath()

        if not os.path.isdir(os.path.dirname(path)):
            dlg = wx.MessageDialog(
                self,
                "Invalid Path\n\nThe following path is invalid or does not exist: \n%s\n\nPlease verify path location pyfa's preferences." % path,
                "Error",
                wx.OK | wx.ICON_ERROR
            )

            if dlg.ShowModal() == wx.ID_OK:
                return

        self.progressDialog = wx.ProgressDialog(
            "Backup fits",
            "Generating HTML file at: %s" % path,
            maximum=max_, parent=self,
            style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME
        )

        exportHtml.getInstance().refreshFittingHtml(True, self.backupCallback)
        self.progressDialog.ShowModal()

    def backupCallback(self, info):
        if info == -1:
            self.closeProgressDialog()
        else:
            self.progressDialog.Update(info)

    def fileImportCallback(self, action, data=None):
        """
        While importing fits from file, the logic calls back to this function to
        update progress bar to show activity. XML files can contain multiple
        ships with multiple fits, whereas EFT cfg files contain many fits of
        a single ship. When iterating through the files, we update the message
        when we start a new file, and then Pulse the progress bar with every fit
        that is processed.

        action : a flag that lets us know how to deal with :data
                None: Pulse the progress bar
                1: Replace message with data
                other: Close dialog and handle based on :action (-1 open fits, -2 display error)
        """

        if action is None:
            self.progressDialog.Pulse()
        elif action == 1 and data != self.progressDialog.message:
            self.progressDialog.message = data
            self.progressDialog.Pulse(data)
        else:
            self.closeProgressDialog()
            if action == -1:
                self._openAfterImport(data)
            elif action == -2:
                dlg = wx.MessageDialog(self,
                                       "The following error was generated\n\n%s\n\nBe aware that already processed fits were not saved" % data,
                                       "Import Error", wx.OK | wx.ICON_ERROR)
                if dlg.ShowModal() == wx.ID_OK:
                    return

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
        dlg = wx.FileDialog(
            self,
            "Open One Or More Character Files",
            wildcard="EVE API XML character files (*.xml)|*.xml|All Files (*)|*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        )

        if dlg.ShowModal() == wx.ID_OK:
            self.waitDialog = wx.BusyInfo("Importing Character...")
            sCharacter = Character.getInstance()
            sCharacter.importCharacter(dlg.GetPaths(), self.importCharacterCallback)

    def importCharacterCallback(self):
        self.closeWaitDialog()
        wx.PostEvent(self, GE.CharListUpdated())

    def closeWaitDialog(self):
        del self.waitDialog

    def openGraphFrame(self, event):
        global graphFrame_enabled

        if not self.graphFrame:
            self.graphFrame = GraphFrame(self)

            if graphFrame_enabled:
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


class MainMenuBar(wx.MenuBar):
    def __init__(self):
        self.characterEditorId = wx.NewId()
        self.damagePatternEditorId = wx.NewId()
        self.targetResistsEditorId = wx.NewId()
        self.implantSetEditorId = wx.NewId()
        self.graphFrameId = wx.NewId()
        self.backupFitsId = wx.NewId()
        self.exportSkillsNeededId = wx.NewId()
        self.importCharacterId = wx.NewId()
        self.exportHtmlId = wx.NewId()
        self.wikiId = wx.NewId()
        self.forumId = wx.NewId()
        self.saveCharId = wx.NewId()
        self.saveCharAsId = wx.NewId()
        self.revertCharId = wx.NewId()
        self.eveFittingsId = wx.NewId()
        self.exportToEveId = wx.NewId()
        self.ssoLoginId = wx.NewId()
        self.attrEditorId = wx.NewId()
        self.toggleOverridesId = wx.NewId()
        self.importDatabaseDefaultsId = wx.NewId()

        if 'wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0):
            wx.ID_COPY = wx.NewId()
            wx.ID_PASTE = wx.NewId()

        self.mainFrame = MainFrame.getInstance()
        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        self.Append(fileMenu, "&File")

        fileMenu.Append(self.mainFrame.addPageId, "&New Tab\tCTRL+T", "Open a new fitting tab")
        fileMenu.Append(self.mainFrame.closePageId, "&Close Tab\tCTRL+W", "Close the current fit")
        fileMenu.AppendSeparator()

        fileMenu.Append(self.backupFitsId, "&Backup All Fittings", "Backup all fittings to a XML file")
        fileMenu.Append(wx.ID_OPEN, "&Import Fittings\tCTRL+O", "Import fittings into pyfa")
        fileMenu.Append(wx.ID_SAVEAS, "&Export Fitting\tCTRL+S", "Export fitting to another format")
        fileMenu.AppendSeparator()
        fileMenu.Append(self.exportHtmlId, "Export HTML", "Export fits to HTML file (set in Preferences)")
        fileMenu.Append(self.exportSkillsNeededId, "Export &Skills Needed", "Export skills needed for this fitting")
        fileMenu.Append(self.importCharacterId, "Import C&haracter File", "Import characters into pyfa from file")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_EXIT)

        # Edit menu
        editMenu = wx.Menu()
        self.Append(editMenu, "&Edit")

        # editMenu.Append(wx.ID_UNDO)
        # editMenu.Append(wx.ID_REDO)

        editMenu.Append(wx.ID_COPY, "To Clipboard\tCTRL+C", "Export a fit to the clipboard")
        editMenu.Append(wx.ID_PASTE, "From Clipboard\tCTRL+V", "Import a fit from the clipboard")
        editMenu.AppendSeparator()
        editMenu.Append(self.saveCharId, "Save Character")
        editMenu.Append(self.saveCharAsId, "Save Character As...")
        editMenu.Append(self.revertCharId, "Revert Character")

        # Character menu
        windowMenu = wx.Menu()
        self.Append(windowMenu, "&Window")

        charEditItem = wx.MenuItem(windowMenu, self.characterEditorId, "&Character Editor\tCTRL+E")
        charEditItem.SetBitmap(BitmapLoader.getBitmap("character_small", "gui"))
        windowMenu.AppendItem(charEditItem)

        damagePatternEditItem = wx.MenuItem(windowMenu, self.damagePatternEditorId, "Damage Pattern Editor\tCTRL+D")
        damagePatternEditItem.SetBitmap(BitmapLoader.getBitmap("damagePattern_small", "gui"))
        windowMenu.AppendItem(damagePatternEditItem)

        targetResistsEditItem = wx.MenuItem(windowMenu, self.targetResistsEditorId, "Target Resists Editor\tCTRL+R")
        targetResistsEditItem.SetBitmap(BitmapLoader.getBitmap("explosive_small", "gui"))
        windowMenu.AppendItem(targetResistsEditItem)

        implantSetEditItem = wx.MenuItem(windowMenu, self.implantSetEditorId, "Implant Set Editor\tCTRL+I")
        implantSetEditItem.SetBitmap(BitmapLoader.getBitmap("hardwire_small", "gui"))
        windowMenu.AppendItem(implantSetEditItem)

        graphFrameItem = wx.MenuItem(windowMenu, self.graphFrameId, "Graphs\tCTRL+G")
        graphFrameItem.SetBitmap(BitmapLoader.getBitmap("graphs_small", "gui"))
        windowMenu.AppendItem(graphFrameItem)

        preferencesShortCut = "CTRL+," if 'wxMac' in wx.PlatformInfo else "CTRL+P"
        preferencesItem = wx.MenuItem(windowMenu, wx.ID_PREFERENCES, "Preferences\t" + preferencesShortCut)
        preferencesItem.SetBitmap(BitmapLoader.getBitmap("preferences_small", "gui"))
        windowMenu.AppendItem(preferencesItem)

        if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
            self.sCrest = Crest.getInstance()

            # CREST Menu
            crestMenu = wx.Menu()
            self.Append(crestMenu, "&CREST")
            if self.sCrest.settings.get('mode') != CrestModes.IMPLICIT:
                crestMenu.Append(self.ssoLoginId, "Manage Characters")
            else:
                crestMenu.Append(self.ssoLoginId, "Login to EVE")
            crestMenu.Append(self.eveFittingsId, "Browse EVE Fittings")
            crestMenu.Append(self.exportToEveId, "Export To EVE")

            if self.sCrest.settings.get('mode') == CrestModes.IMPLICIT or len(self.sCrest.getCrestCharacters()) == 0:
                self.Enable(self.eveFittingsId, False)
                self.Enable(self.exportToEveId, False)

            if not disableOverrideEditor:
                windowMenu.AppendSeparator()
                attrItem = wx.MenuItem(windowMenu, self.attrEditorId, "Attribute Overrides\tCTRL+B")
                attrItem.SetBitmap(BitmapLoader.getBitmap("fit_rename_small", "gui"))
                windowMenu.AppendItem(attrItem)
                windowMenu.Append(self.toggleOverridesId, "Turn Overrides On")

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, "&Help")
        helpMenu.Append(self.wikiId, "Wiki", "Go to wiki on GitHub")
        helpMenu.Append(self.forumId, "Forums", "Go to EVE Online Forum thread")
        helpMenu.AppendSeparator()
        helpMenu.Append(self.importDatabaseDefaultsId, "Import D&atabase Defaults", "Imports missing database defaults")
        helpMenu.AppendSeparator()
        helpMenu.Append(wx.ID_ABOUT)

        if config.debug:
            helpMenu.Append(self.mainFrame.widgetInspectMenuID, "Open Widgets Inspect tool",
                            "Open Widgets Inspect tool")

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    def fitChanged(self, event):
        enable = event.fitID is not None
        self.Enable(wx.ID_SAVEAS, enable)
        self.Enable(wx.ID_COPY, enable)
        self.Enable(self.exportSkillsNeededId, enable)

        sChar = Character.getInstance()
        charID = self.mainFrame.charSelection.getActiveCharacter()
        char = sChar.getCharacter(charID)

        # enable/disable character saving stuff
        self.Enable(self.saveCharId, not char.ro and char.isDirty)
        self.Enable(self.saveCharAsId, char.isDirty)
        self.Enable(self.revertCharId, char.isDirty)

        event.Skip()


class GraphFrame(wx.Frame):
    def __init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE | wx.FRAME_FLOAT_ON_PARENT):

        global graphFrame_enabled
        global mplImported

        self.legendFix = False
        if not graphFrame_enabled:
            return

        try:
            cache_dir = mpl._get_cachedir()
        except:
            cache_dir = os.path.expanduser(os.path.join("~", ".matplotlib"))

        cache_file = parsePath(cache_dir, 'fontList.cache')

        if os.access(cache_dir, os.W_OK | os.X_OK) and os.path.isfile(cache_file):
            # remove matplotlib font cache, see #234
            os.remove(cache_file)
        if not mplImported:
            mpl.use('wxagg')

        graphFrame_enabled = True
        if mpl.__version__[0] != "1":
            print("pyfa: Found matplotlib version ", mpl.__version__, " - activating OVER9000 workarounds")
            print("pyfa: Recommended minimum matplotlib version is 1.0.0")
            self.legendFix = True

        mplImported = True

        wx.Frame.__init__(self, parent, title=u"pyfa: Graph Generator", style=style, size=(520, 390))

        i = wx.IconFromBitmap(BitmapLoader.getBitmap("graphs_small", "gui"))
        self.SetIcon(i)
        self.mainFrame = MainFrame.getInstance()
        self.CreateStatusBar()

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.mainSizer)

        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())
        self.fits = [fit] if fit is not None else []
        self.fitList = FitList(self)
        self.fitList.SetMinSize((270, -1))

        self.fitList.fitList.update(self.fits)

        self.graphSelection = wx.Choice(self, wx.ID_ANY, style=0)
        self.mainSizer.Add(self.graphSelection, 0, wx.EXPAND)

        self.figure = Figure(figsize=(4, 3))

        rgbtuple = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE).Get()
        clr = [c / 255. for c in rgbtuple]
        self.figure.set_facecolor(clr)
        self.figure.set_edgecolor(clr)

        self.canvas = Canvas(self, -1, self.figure)
        self.canvas.SetBackgroundColour(wx.Colour(*rgbtuple))

        self.subplot = self.figure.add_subplot(111)
        self.subplot.grid(True)

        self.mainSizer.Add(self.canvas, 1, wx.EXPAND)
        self.mainSizer.Add(wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL), 0,
                           wx.EXPAND)

        self.gridPanel = wx.Panel(self)
        self.mainSizer.Add(self.gridPanel, 0, wx.EXPAND)

        dummyBox = wx.BoxSizer(wx.VERTICAL)
        self.gridPanel.SetSizer(dummyBox)

        self.gridSizer = wx.FlexGridSizer(0, 4)
        self.gridSizer.AddGrowableCol(1)
        dummyBox.Add(self.gridSizer, 0, wx.EXPAND)

        for view in Graph.views:
            view = view()
            self.graphSelection.Append(view.name, view)

        self.graphSelection.SetSelection(0)
        self.fields = {}
        self.select(0)
        self.sl1 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.mainSizer.Add(self.sl1, 0, wx.EXPAND)
        self.mainSizer.Add(self.fitList, 0, wx.EXPAND)

        self.fitList.fitList.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.draw)
        self.Bind(wx.EVT_CLOSE, self.close)

        self.Fit()
        self.SetMinSize(self.GetSize())

    def handleDrag(self, type, fitID):
        if type == "fit":
            self.AppendFitToList(fitID)

    def close(self, event):
        self.fitList.fitList.Unbind(wx.EVT_LEFT_DCLICK, handler=self.removeItem)
        self.mainFrame.Unbind(GE.FIT_CHANGED, handler=self.draw)
        event.Skip()

    def getView(self):
        return self.graphSelection.GetClientData(self.graphSelection.GetSelection())

    def getValues(self):
        values = {}
        for fieldName, field in self.fields.iteritems():
            values[fieldName] = field.GetValue()

        return values

    def select(self, index):
        view = self.getView()
        icons = view.getIcons()
        labels = view.getLabels()
        sizer = self.gridSizer
        self.gridPanel.DestroyChildren()
        self.fields.clear()

        # Setup textboxes
        for field, defaultVal in view.getFields().iteritems():

            textBox = wx.TextCtrl(self.gridPanel, wx.ID_ANY, style=0)
            self.fields[field] = textBox
            textBox.Bind(wx.EVT_TEXT, self.onFieldChanged)
            sizer.Add(textBox, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            if defaultVal is not None:
                if not isinstance(defaultVal, basestring):
                    defaultVal = ("%f" % defaultVal).rstrip("0")
                    if defaultVal[-1:] == ".":
                        defaultVal += "0"

                textBox.ChangeValue(defaultVal)

            imgLabelSizer = wx.BoxSizer(wx.HORIZONTAL)
            if icons:
                icon = icons.get(field)
                if icon is not None:
                    static = wx.StaticBitmap(self.gridPanel)
                    static.SetBitmap(icon)
                    imgLabelSizer.Add(static, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 1)

            if labels:
                label = labels.get(field)
                label = label if label is not None else field
            else:
                label = field

            imgLabelSizer.Add(wx.StaticText(self.gridPanel, wx.ID_ANY, label), 0,
                              wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
            sizer.Add(imgLabelSizer, 0, wx.ALIGN_CENTER_VERTICAL)
        self.draw()

    def draw(self, event=None):
        values = self.getValues()
        view = self.getView()
        self.subplot.clear()
        self.subplot.grid(True)
        legend = []

        for fit in self.fits:
            try:
                success, status = view.getPoints(fit, values)
                if not success:
                    # TODO: Add a pwetty statys bar to report errors with
                    self.SetStatusText(status)
                    return

                x, y = success, status

                self.subplot.plot(x, y)
                legend.append(fit.name)
            except:
                self.SetStatusText("Invalid values in '%s'" % fit.name)
                self.canvas.draw()
                return

        if self.legendFix and len(legend) > 0:
            leg = self.subplot.legend(tuple(legend), "upper right", shadow=False)
            for t in leg.get_texts():
                t.set_fontsize('small')

            for l in leg.get_lines():
                l.set_linewidth(1)

        elif not self.legendFix and len(legend) > 0:
            leg = self.subplot.legend(tuple(legend), "upper right", shadow=False, frameon=False)
            for t in leg.get_texts():
                t.set_fontsize('small')

            for l in leg.get_lines():
                l.set_linewidth(1)

        self.canvas.draw()
        self.SetStatusText("")
        if event is not None:
            event.Skip()

    def onFieldChanged(self, event):
        self.draw()

    def AppendFitToList(self, fitID):
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit not in self.fits:
            self.fits.append(fit)

        self.fitList.fitList.update(self.fits)
        self.draw()

    def removeItem(self, event):
        row, _ = self.fitList.fitList.HitTest(event.Position)
        if row != -1:
            del self.fits[row]
            self.fitList.fitList.update(self.fits)
            self.draw()
