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

import datetime
import os.path
import threading
import time
import webbrowser
from codecs import open
from time import gmtime, strftime

# noinspection PyPackageRequirements
import wx
import wx.adv
from logbook import Logger
# noinspection PyPackageRequirements
from wx.lib.inspection import InspectionTool

import config
import gui.fitCommands as cmd
import gui.globalEvents as GE
from eos.config import gamedata_date, gamedata_version
from eos.modifiedAttributeDict import ModifiedAttributeDict
from graphs import GraphFrame
from gui.additionsPane import AdditionsPane
from gui.bitmap_loader import BitmapLoader
from gui.builtinMarketBrowser.events import ItemSelected
from gui.builtinShipBrowser.events import FitSelected, ImportSelected, Stage3Selected
# noinspection PyUnresolvedReferences
from gui.builtinViews import emptyView, entityEditor, fittingView, implantEditor  # noqa: F401
from gui.characterEditor import CharacterEditor
from gui.characterSelection import CharacterSelection
from gui.chrome_tabs import ChromeNotebook
from gui.copySelectDialog import CopySelectDialog
from gui.devTools import DevTools
from gui.esiFittings import EveFittings, ExportToEve, SsoCharacterMgmt
from gui.mainMenuBar import MainMenuBar
from gui.marketBrowser import MarketBrowser
from gui.multiSwitch import MultiSwitch
from gui.patternEditor import DmgPatternEditor
from gui.preferenceDialog import PreferenceDialog
from gui.setEditor import ImplantSetEditor
from gui.shipBrowser import ShipBrowser
from gui.statsPane import StatsPane
from gui.targetProfileEditor import TargetProfileEditor
from gui.updateDialog import UpdateDialog
from gui.utils.clipboard import fromClipboard
from service.character import Character
from service.esi import Esi
from service.fit import Fit
from service.port import IPortUser, Port
from service.price import Price
from service.settings import HTMLExportSettings, SettingsProvider
from service.update import Update

_t = wx.GetTranslation

pyfalog = Logger(__name__)

disableOverrideEditor = False

try:
    from gui.propertyEditor import AttributeEditor
except ImportError as e:
    AttributeEditor = None
    pyfalog.warning("Error loading Attribute Editor: %s.\nAccess to Attribute Editor is disabled." % e.message)
    disableOverrideEditor = True

pyfalog.debug("Done loading mainframe imports")


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
        self.running = True
        self.start()

    def run(self):
        # `startup` tells FitSpawner that we are loading fits are startup, and
        # has 3 values:
        # False = Set as default in FitSpawner itself, never set here
        # 1 = Create new fit page, but do not calculate page
        # 2 = Create new page and calculate
        # We use 1 for all fits except the last one where we use 2 so that we
        # have correct calculations displayed at startup
        for fitID in self.fits[:-1]:
            if self.running:
                wx.PostEvent(self.mainFrame, FitSelected(fitID=fitID, startup=1))

        if self.running:
            wx.PostEvent(self.mainFrame, FitSelected(fitID=self.fits[-1], startup=2))
            wx.CallAfter(self.callback)

    def stop(self):
        self.running = False


# todo: include IPortUser again
class MainFrame(wx.Frame):
    __instance = None

    @classmethod
    def getInstance(cls):
        return cls.__instance if cls.__instance is not None else MainFrame()

    def __init__(self, title="pyfa"):
        pyfalog.debug("Initialize MainFrame")
        self.title = title
        super().__init__(None, wx.ID_ANY, self.title)

        self.supress_left_up = False

        MainFrame.__instance = self

        # Load stored settings (width/height/maximized..)
        self.LoadMainFrameAttribs()

        self.disableOverrideEditor = disableOverrideEditor

        # Fix for msw (have the frame background color match panel color
        if 'wxMSW' in wx.PlatformInfo:
            self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        # Load and set the icon for pyfa main window
        i = wx.Icon(BitmapLoader.getBitmap("pyfa", "gui"))
        self.SetIcon(i)

        # Create the layout and windows
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.browser_fitting_split = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.fitting_additions_split = wx.SplitterWindow(self.browser_fitting_split, style=wx.SP_LIVE_UPDATE)

        mainSizer.Add(self.browser_fitting_split, 1, wx.EXPAND | wx.LEFT, 2)

        self.fitMultiSwitch = MultiSwitch(self.fitting_additions_split)
        self.additionsPane = AdditionsPane(self.fitting_additions_split, self)

        self.notebookBrowsers = ChromeNotebook(self.browser_fitting_split, False)

        marketImg = BitmapLoader.getImage("market_small", "gui")
        shipBrowserImg = BitmapLoader.getImage("ship_small", "gui")

        self.marketBrowser = MarketBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.marketBrowser, _t("Market"), image=marketImg, closeable=False)
        self.marketBrowser.splitter.SetSashPosition(self.marketHeight)

        self.shipBrowser = ShipBrowser(self.notebookBrowsers)
        self.notebookBrowsers.AddPage(self.shipBrowser, _t("Fittings"), image=shipBrowserImg, closeable=False)

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

        # @todo pheonix: fix all stats stuff
        self.statsPane = StatsPane(self)
        cstatsSizer.Add(self.statsPane, 0, wx.EXPAND)

        mainSizer.Add(cstatsSizer, 0, wx.EXPAND)

        self.SetSizer(mainSizer)

        # Add menu
        self.addPageId = wx.NewId()
        self.closePageId = wx.NewId()
        self.closeAllPagesId = wx.NewId()
        self.hiddenGraphsId = wx.NewId()

        self.widgetInspectMenuID = wx.NewId()
        self.SetMenuBar(MainMenuBar(self))
        self.registerMenu()

        # Internal vars to keep track of other windows
        self.statsWnds = []
        self.activeStatsWnd = None

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Show ourselves
        self.Show()

        self.LoadPreviousOpenFits()

        # Check for updates
        self.sUpdate = Update.getInstance()
        self.sUpdate.CheckUpdate(self.ShowUpdateBox)

        self.Bind(GE.EVT_SSO_LOGIN, self.onSSOLogin)

    @property
    def command(self) -> wx.CommandProcessor:
        return Fit.getCommandProcessor(self.getActiveFit())

    def getCommandForFit(self, fitID) -> wx.CommandProcessor:
        return Fit.getCommandProcessor(fitID)

    def ShowUpdateBox(self, release, version):
        with UpdateDialog(self, release, version) as dlg:
            dlg.ShowModal()

    def LoadPreviousOpenFits(self):
        sFit = Fit.getInstance()

        self.prevOpenFits = SettingsProvider.getInstance().getSettings("pyfaPrevOpenFits",
                                                                       {"enabled": False, "pyfaOpenFits": []})
        fits = self.prevOpenFits['pyfaOpenFits']

        # Remove any fits that cause exception when fetching (non-existent fits)
        for id in fits[:]:
            try:
                fit = sFit.getFit(id, basic=True)
                if fit is None:
                    fits.remove(id)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                fits.remove(id)

        if not self.prevOpenFits['enabled'] or len(fits) == 0:
            # add blank page if there are no fits to be loaded
            self.fitMultiSwitch.AddPage()
            return

        self.waitDialog = wx.BusyInfo(_t("Loading previous fits..."), parent=self)
        OpenFitsThread(fits, self.closeWaitDialog)

    def _getDisplayData(self):
        displayData = []
        for i in range(wx.Display.GetCount()):
            display = wx.Display(i)
            displayData.append(display.GetClientArea())
        return displayData

    def LoadMainFrameAttribs(self):
        mainFrameDefaultAttribs = {
            "wnd_display": 0, "wnd_x": 0, "wnd_y": 0, "wnd_width": 1000, "wnd_height": 700, "wnd_maximized": False,
            "browser_width": 300, "market_height": 0, "fitting_height": -200
        }
        self.mainFrameAttribs = SettingsProvider.getInstance().getSettings(
                "pyfaMainWindowAttribs", mainFrameDefaultAttribs)

        wndDisplay = self.mainFrameAttribs["wnd_display"]
        displayData = self._getDisplayData()
        try:
            selectedDisplayData = displayData[wndDisplay]
        except IndexError:
            selectedDisplayData = displayData[0]
        dspX, dspY, dspW, dspH = selectedDisplayData

        if self.mainFrameAttribs["wnd_maximized"]:
            wndW = mainFrameDefaultAttribs["wnd_width"]
            wndH = mainFrameDefaultAttribs["wnd_height"]
            wndX = min(mainFrameDefaultAttribs["wnd_x"], dspW * 0.75)
            wndY = min(mainFrameDefaultAttribs["wnd_y"], dspH * 0.75)
            self.Maximize()
        else:
            wndW = self.mainFrameAttribs["wnd_width"]
            wndH = self.mainFrameAttribs["wnd_height"]
            wndX = min(self.mainFrameAttribs["wnd_x"], dspW * 0.75)
            wndY = min(self.mainFrameAttribs["wnd_y"], dspH * 0.75)

        self.SetPosition((dspX + wndX, dspY + wndY))
        self.SetSize((wndW, wndH))
        self.SetMinSize((mainFrameDefaultAttribs["wnd_width"], mainFrameDefaultAttribs["wnd_height"]))

        self.browserWidth = self.mainFrameAttribs["browser_width"]
        self.marketHeight = self.mainFrameAttribs["market_height"]
        self.fittingHeight = self.mainFrameAttribs["fitting_height"]

    def UpdateMainFrameAttribs(self):
        if self.IsIconized():
            return

        wndGlobalX, wndGlobalY = self.GetPosition()
        displayData = self._getDisplayData()
        wndDisplay = 0
        wndX = 0
        wndY = 0
        for i, (sdX, sdY, sdW, sdH) in enumerate(displayData):
            wndRelX = wndGlobalX - sdX
            wndRelY = wndGlobalY - sdY
            if 0 <= wndRelX < sdW and 0 <= wndRelY < sdH:
                wndDisplay = i
                wndX = wndRelX
                wndY = wndRelY
                break
        self.mainFrameAttribs["wnd_display"] = wndDisplay
        self.mainFrameAttribs["wnd_x"] = wndX
        self.mainFrameAttribs["wnd_y"] = wndY

        wndW, wndH = self.GetSize()
        self.mainFrameAttribs["wnd_width"] = wndW
        self.mainFrameAttribs["wnd_height"] = wndH
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

    def CloseAllPages(self, evt):
        ms = self.fitMultiSwitch
        for _ in range(ms.GetPageCount()):
            ms.DeletePage(0)

    def OnClose(self, event):
        self.UpdateMainFrameAttribs()

        # save open fits
        self.prevOpenFits['pyfaOpenFits'] = []  # clear old list
        for page in self.fitMultiSwitch._pages:
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
        info = wx.adv.AboutDialogInfo()
        info.Name = "pyfa"
        time = datetime.datetime.fromtimestamp(int(gamedata_date)).strftime('%Y-%m-%d %H:%M:%S')
        info.Version = config.getVersion() + '\nEVE Data Version: {} ({})'.format(gamedata_version, time)  # gui.aboutData.versionString
        #
        # try:
        #     import matplotlib
        #     matplotlib_version = matplotlib.__version__
        # except:
        #     matplotlib_version = None
        #
        # info.Description = wordwrap(gui.aboutData.description + _("\n\nDevelopers:\n\t") +
        #                             "\n\t".join(gui.aboutData.developers) +
        #                             "\n\nAdditional credits:\n\t" +
        #                             "\n\t".join(gui.aboutData.credits) +
        #                             "\n\nLicenses:\n\t" +
        #                             "\n\t".join(gui.aboutData.licenses) +
        #                             "\n\nEVE Data: \t" + gamedata_version +
        #                             "\nPython: \t\t" + '{}.{}.{}'.format(v.major, v.minor, v.micro) +
        #                             "\nwxPython: \t" + wx.__version__ +
        #                             "\nSQLAlchemy: \t" + sqlalchemy.__version__ +
        #                             "\nmatplotlib: \t {}".format(matplotlib_version if matplotlib_version else "Not Installed"),
        #                             500, wx.ClientDC(self))
        # if "__WXGTK__" in wx.PlatformInfo:
        #     forumUrl = "http://forums.eveonline.com/default.aspx?g=posts&amp;t=466425"
        # else:
        #     forumUrl = "http://forums.eveonline.com/default.aspx?g=posts&t=466425"
        # info.WebSite = (forumUrl, "pyfa thread at EVE Online forum")
        wx.adv.AboutBox(info)

    def OnShowGraphFrame(self, event):
        GraphFrame.openOne(self)

    def OnShowGraphFrameHidden(self, event):
        GraphFrame.openOne(self, includeHidden=True)

    def OnShowDevTools(self, event):
        DevTools.openOne(parent=self)

    def OnShowCharacterEditor(self, event):
        CharacterEditor.openOne(parent=self)

    def OnShowAttrEditor(self, event):
        AttributeEditor.openOne(parent=self)

    def OnShowTargetProfileEditor(self, event):
        TargetProfileEditor.openOne(parent=self)

    def OnShowDamagePatternEditor(self, event):
        DmgPatternEditor.openOne(parent=self)

    def OnShowImplantSetEditor(self, event):
        ImplantSetEditor.openOne(parent=self)

    def OnShowExportDialog(self, event):
        """ Export active fit """
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.getActiveFit())
        defaultFile = "%s - %s.xml" % (fit.ship.item.name, fit.name) if fit else None

        with wx.FileDialog(
                self, _t("Save Fitting As..."),
                wildcard=_t("EVE XML fitting files") + " (*.xml)|*.xml",
                style=wx.FD_SAVE,
                defaultFile=defaultFile
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.supress_left_up = True
                format_ = dlg.GetFilterIndex()
                path = dlg.GetPath()
                if format_ == 0:
                    output = Port.exportXml([fit], None)
                    if '.' not in os.path.basename(path):
                        path += ".xml"
                    with open(path, "w", encoding="utf-8") as openfile:
                        openfile.write(output)
                        openfile.close()
                else:
                    pyfalog.warning("oops, invalid fit format %d" % format_)
                    return

    def OnShowPreferenceDialog(self, event):
        with PreferenceDialog(self) as dlg:
            dlg.ShowModal()

    @staticmethod
    def goWiki(event):
        webbrowser.open('https://github.com/pyfa-org/Pyfa/wiki')

    @staticmethod
    def goForums(event):
        webbrowser.open('https://forums.eveonline.com/t/27156')

    def registerMenu(self):
        menuBar = self.GetMenuBar()
        # Quit
        self.Bind(wx.EVT_MENU, self.ExitApp, id=wx.ID_EXIT)
        # Widgets Inspector
        if config.debug:
            self.Bind(wx.EVT_MENU, self.openWXInspectTool, id=self.widgetInspectMenuID)
            self.Bind(wx.EVT_MENU, self.OnShowDevTools, id=menuBar.devToolsId)
        # About
        self.Bind(wx.EVT_MENU, self.ShowAboutBox, id=wx.ID_ABOUT)
        # Char editor
        self.Bind(wx.EVT_MENU, self.OnShowCharacterEditor, id=menuBar.characterEditorId)
        # Damage pattern editor
        self.Bind(wx.EVT_MENU, self.OnShowDamagePatternEditor, id=menuBar.damagePatternEditorId)
        # Target Profile editor
        self.Bind(wx.EVT_MENU, self.OnShowTargetProfileEditor, id=menuBar.targetProfileEditorId)
        # Implant Set editor
        self.Bind(wx.EVT_MENU, self.OnShowImplantSetEditor, id=menuBar.implantSetEditorId)
        # Import dialog
        self.Bind(wx.EVT_MENU, self.fileImportDialog, id=wx.ID_OPEN)
        # Export dialog
        self.Bind(wx.EVT_MENU, self.OnShowExportDialog, id=wx.ID_SAVEAS)
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
        self.Bind(wx.EVT_MENU, self.OnShowPreferenceDialog, id=wx.ID_PREFERENCES)
        # User guide
        self.Bind(wx.EVT_MENU, self.goWiki, id=menuBar.wikiId)

        self.Bind(wx.EVT_MENU, lambda evt: MainFrame.getInstance().command.Undo(), id=wx.ID_UNDO)

        self.Bind(wx.EVT_MENU, lambda evt: MainFrame.getInstance().command.Redo(), id=wx.ID_REDO)
        # EVE Forums
        self.Bind(wx.EVT_MENU, self.goForums, id=menuBar.forumId)
        # Save current character
        self.Bind(wx.EVT_MENU, self.saveChar, id=menuBar.saveCharId)
        # Save current character as another character
        self.Bind(wx.EVT_MENU, self.saveCharAs, id=menuBar.saveCharAsId)
        # Save current character
        self.Bind(wx.EVT_MENU, self.revertChar, id=menuBar.revertCharId)
        # Optimize fit price
        self.Bind(wx.EVT_MENU, self.optimizeFitPrice, id=menuBar.optimizeFitPrice)

        # Browse fittings
        self.Bind(wx.EVT_MENU, self.eveFittings, id=menuBar.eveFittingsId)
        # Export to EVE
        self.Bind(wx.EVT_MENU, self.exportToEve, id=menuBar.exportToEveId)
        # Handle SSO event (login/logout/manage characters, depending on mode and current state)
        self.Bind(wx.EVT_MENU, self.ssoHandler, id=menuBar.ssoLoginId)

        # Open attribute editor
        self.Bind(wx.EVT_MENU, self.OnShowAttrEditor, id=menuBar.attrEditorId)
        # Toggle Overrides
        self.Bind(wx.EVT_MENU, self.toggleOverrides, id=menuBar.toggleOverridesId)

        # Clipboard exports
        self.Bind(wx.EVT_MENU, self.exportToClipboard, id=wx.ID_COPY)

        # Fitting Restrictions
        self.Bind(wx.EVT_MENU, self.toggleIgnoreRestriction, id=menuBar.toggleIgnoreRestrictionID)

        # Graphs
        self.Bind(wx.EVT_MENU, self.OnShowGraphFrame, id=menuBar.graphFrameId)
        self.Bind(wx.EVT_MENU, self.OnShowGraphFrameHidden, id=self.hiddenGraphsId)

        toggleSearchBoxId = wx.NewId()
        toggleShipMarketId = wx.NewId()
        ctabnext = wx.NewId()
        ctabprev = wx.NewId()

        # Close Page
        self.Bind(wx.EVT_MENU, self.CloseCurrentPage, id=self.closePageId)
        self.Bind(wx.EVT_MENU, self.CloseAllPages, id=self.closeAllPagesId)
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

                (wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("G"), self.hiddenGraphsId),
                (wx.ACCEL_CMD | wx.ACCEL_ALT, ord("G"), self.hiddenGraphsId),

                (wx.ACCEL_CTRL | wx.ACCEL_ALT, ord("W"), self.closeAllPagesId),
                (wx.ACCEL_CTRL | wx.ACCEL_ALT, wx.WXK_F4, self.closeAllPagesId),
                (wx.ACCEL_CMD | wx.ACCEL_ALT, ord("W"), self.closeAllPagesId),

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
                (wx.ACCEL_CMD, wx.WXK_PAGEUP, ctabprev),

                (wx.ACCEL_CMD | wx.ACCEL_SHIFT, ord("Z"), wx.ID_REDO)
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

    def toggleIgnoreRestriction(self, event):

        sFit = Fit.getInstance()
        fitID = self.getActiveFit()
        fit = sFit.getFit(fitID)

        if not fit.ignoreRestrictions:
            with wx.MessageDialog(
                    self, _t("Are you sure you wish to ignore fitting restrictions for the "
                             "current fit? This could lead to wildly inaccurate results and possible errors."),
                    _t("Confirm"), wx.YES_NO | wx.ICON_QUESTION
            ) as dlg:
                result = dlg.ShowModal() == wx.ID_YES
        else:
            with wx.MessageDialog(
                    self, _t("Re-enabling fitting restrictions for this fit will also remove any illegal items "
                             "from the fit. Do you want to continue?"), _t("Confirm"), wx.YES_NO | wx.ICON_QUESTION
            ) as dlg:
                result = dlg.ShowModal() == wx.ID_YES
        if result:
            self.command.Submit(cmd.GuiToggleFittingRestrictionsCommand(fitID=fitID))

    def eveFittings(self, event):
        EveFittings.openOne(parent=self)

    def onSSOLogin(self, event):
        menu = self.GetMenuBar()
        menu.Enable(menu.eveFittingsId, True)
        menu.Enable(menu.exportToEveId, True)

    def updateEsiMenus(self, type):
        menu = self.GetMenuBar()
        sEsi = Esi.getInstance()

        menu.SetLabel(menu.ssoLoginId, _t("Manage Characters"))
        enable = len(sEsi.getSsoCharacters()) == 0
        menu.Enable(menu.eveFittingsId, not enable)
        menu.Enable(menu.exportToEveId, not enable)

    def ssoHandler(self, event):
        SsoCharacterMgmt.openOne(parent=self)

    def exportToEve(self, event):
        ExportToEve.openOne(parent=self)

    def toggleOverrides(self, event):
        ModifiedAttributeDict.overrides_enabled = not ModifiedAttributeDict.overrides_enabled
        changedFitIDs = Fit.getInstance().processOverrideToggle()
        wx.PostEvent(self, GE.FitChanged(fitIDs=changedFitIDs))
        menu = self.GetMenuBar()
        menu.SetLabel(menu.toggleOverridesId,
                      _t("&Turn Overrides Off") if ModifiedAttributeDict.overrides_enabled else _t("&Turn Overrides On"))

    def saveChar(self, event):
        sChr = Character.getInstance()
        charID = self.charSelection.getActiveCharacter()
        sChr.saveCharacter(charID)
        wx.PostEvent(self, GE.CharListUpdated())

    def saveCharAs(self, event):
        charID = self.charSelection.getActiveCharacter()
        CharacterEditor.SaveCharacterAs(self, charID)
        wx.PostEvent(self, GE.CharListUpdated())

    def revertChar(self, event):
        sChr = Character.getInstance()
        charID = self.charSelection.getActiveCharacter()
        sChr.revertCharacter(charID)
        wx.PostEvent(self, GE.CharListUpdated())

    def optimizeFitPrice(self, event):
        fitID = self.getActiveFit()
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)

        if fit:
            def updateFitCb(replacementsCheaper):
                del self.waitDialog
                del self.disablerAll
                rebaseMap = {k.ID: v.ID for k, v in replacementsCheaper.items()}
                self.command.Submit(cmd.GuiRebaseItemsCommand(fitID=fitID, rebaseMap=rebaseMap))

            fitItems = {i for i in Fit.fitItemIter(fit, forceFitImplants=True) if i is not fit.ship.item}
            self.disablerAll = wx.WindowDisabler()
            self.waitDialog = wx.BusyInfo(_t("Please Wait..."), parent=self)
            Price.getInstance().findCheaperReplacements(fitItems, updateFitCb, fetchTimeout=10)

    def AdditionsTabSelect(self, event):
        selTab = self.additionsSelect.index(event.GetId())

        if selTab <= self.additionsPane.notebook.GetPageCount():
            self.additionsPane.notebook.SetSelection(selTab)

    def ItemSelect(self, event):
        selItem = self.itemSelect.index(event.GetId())

        activeListing = getattr(self.marketBrowser.itemView, 'active', None)
        if activeListing and selItem < len(activeListing):
            wx.PostEvent(self, ItemSelected(itemID=self.marketBrowser.itemView.active[selItem].ID, allowBatch=False))

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

    def importFromClipboard(self, event):
        clipboard = fromClipboard()
        activeFit = self.getActiveFit()
        try:
            importType, importData = Port().importFitFromBuffer(clipboard, activeFit)
            if importType == "FittingItem":
                baseItem, mutaplasmidItem, mutations = importData[0]
                if mutaplasmidItem:
                    if baseItem.isDrone:
                        self.command.Submit(cmd.GuiImportLocalMutatedDroneCommand(
                            activeFit, baseItem, mutaplasmidItem, mutations, amount=1))
                    else:
                        self.command.Submit(cmd.GuiImportLocalMutatedModuleCommand(
                            activeFit, baseItem, mutaplasmidItem, mutations))
                else:
                    self.command.Submit(cmd.GuiAddLocalModuleCommand(activeFit, baseItem.ID))
                return
            if importType == "AdditionsDrones":
                if self.command.Submit(cmd.GuiImportLocalDronesCommand(activeFit, [(i.ID, a, m) for i, a, m in importData[0]])):
                    self.additionsPane.select("Drones")
                return
            if importType == "AdditionsFighters":
                if self.command.Submit(cmd.GuiImportLocalFightersCommand(activeFit, [(i.ID, a, m) for i, a, m in importData[0]])):
                    self.additionsPane.select("Fighters")
                return
            if importType == "AdditionsImplants":
                if self.command.Submit(cmd.GuiImportImplantsCommand(activeFit, [(i.ID, a, m) for i, a, m in importData[0]])):
                    self.additionsPane.select("Implants")
                return
            if importType == "AdditionsBoosters":
                if self.command.Submit(cmd.GuiImportBoostersCommand(activeFit, [(i.ID, a, m) for i, a, m in importData[0]])):
                    self.additionsPane.select("Boosters")
                return
            if importType == "AdditionsCargo":
                if self.command.Submit(cmd.GuiImportCargosCommand(activeFit, [(i.ID, a, m) for i, a, m in importData[0]])):
                    self.additionsPane.select("Cargo")
                return
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            pyfalog.error("Attempt to import failed:\n{0}", clipboard)
        else:
            self._openAfterImport(importData)

    def exportToClipboard(self, event):
        with CopySelectDialog(self) as dlg:
            dlg.ShowModal()

    def exportSkillsNeeded(self, event):
        """ Exports skills needed for active fit and active character """
        sCharacter = Character.getInstance()
        with wx.FileDialog(
                self,
                _t("Export Skills Needed As..."),
                wildcard=("|".join([
                    _t("EVEMon skills training file") + " (*.emp)|*.emp",
                    _t("EVEMon skills training XML file") + " (*.xml)|*.xml",
                    _t("Text skills training file") + " (*.txt)|*.txt"
                ])),
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                saveFmtInt = dlg.GetFilterIndex()

                if saveFmtInt == 0:  # Per ordering of wildcards above
                    saveFmt = "emp"
                elif saveFmtInt == 1:
                    saveFmt = "xml"
                else:
                    saveFmt = "txt"

                filePath = dlg.GetPath()
                if '.' not in os.path.basename(filePath):
                    filePath += ".{0}".format(saveFmt)

                self.waitDialog = wx.BusyInfo(_t("Exporting skills needed..."), parent=self)
                sCharacter.backupSkills(filePath, saveFmt, self.getActiveFit(), self.closeWaitDialog)

    def fileImportDialog(self, event):
        """Handles importing single/multiple EVE XML / EFT cfg fit files"""
        with wx.FileDialog(
                self,
                _t("Open One Or More Fitting Files"),
                wildcard=("|".join([
                    _t("EVE XML fitting files") + " (*.xml)|*.xml",
                    _t("EFT text fitting files") + " (*.cfg)|*.cfg",
                    _t("All Files") + "|*"
                ])),
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.progressDialog = wx.ProgressDialog(
                        _t("Importing fits"),
                        " " * 100,  # set some arbitrary spacing to create width in window
                        parent=self,
                        style=wx.PD_CAN_ABORT | wx.PD_SMOOTH | wx.PD_ELAPSED_TIME | wx.PD_APP_MODAL
                )
                Port.importFitsThreaded(dlg.GetPaths(), self)
                self.progressDialog.ShowModal()

    def backupToXml(self, event):
        """ Back up all fits to EVE XML file """
        defaultFile = "pyfa-fits-%s.xml" % strftime("%Y%m%d_%H%M%S", gmtime())

        with wx.FileDialog(
                self,
                _t("Save Backup As..."),
                wildcard=_t("EVE XML fitting file") + " (*.xml)|*.xml",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                defaultFile=defaultFile,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                filePath = dlg.GetPath()
                if '.' not in os.path.basename(filePath):
                    filePath += ".xml"

                sFit = Fit.getInstance()
                max_ = sFit.countAllFits()

                self.progressDialog = wx.ProgressDialog(
                        _t("Backup fits"),
                        _t("Backing up {} fits to: {}").format(max_, filePath),
                        maximum=max_,
                        parent=self,
                        style=wx.PD_CAN_ABORT | wx.PD_SMOOTH | wx.PD_ELAPSED_TIME | wx.PD_APP_MODAL
                )
                Port.backupFits(filePath, self)
                self.progressDialog.ShowModal()

    def exportHtml(self, event):
        from gui.utils.exportHtml import exportHtml
        sFit = Fit.getInstance()
        settings = HTMLExportSettings.getInstance()

        max_ = sFit.countAllFits()
        path = settings.getPath()

        if not os.path.isdir(os.path.dirname(path)):
            with wx.MessageDialog(
                    self,
                    _t("Invalid Path") + "\n\n" +
                    _t("The following path is invalid or does not exist:") +
                    f"\n{path}\n\n" +
                    _t("Please verify path location pyfa's preferences."),
                    _t("Error"),
                    wx.OK | wx.ICON_ERROR
            ) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    return

        self.progressDialog = wx.ProgressDialog(
                _t("Backup fits"),
                _t("Generating HTML file at: {}").format(path),
                maximum=max_, parent=self,
                style=wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME)

        exportHtml.getInstance().refreshFittingHtml(True, self.backupCallback)
        self.progressDialog.ShowModal()

    def backupCallback(self, info):
        if info == -1:
            self.closeProgressDialog()
        else:
            self.progressDialog.Update(info)

    def on_port_process_start(self):
        # flag for progress dialog.
        self.__progress_flag = True

    def on_port_processing(self, action, data=None):
        # 2017/03/29 NOTE: implementation like interface
        wx.CallAfter(
                self._on_port_processing, action, data
        )

        return self.__progress_flag

    def _on_port_processing(self, action, data):
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
        _message = None
        if action & IPortUser.ID_ERROR:
            self.closeProgressDialog()
            _message = _t("Import Error") if action & IPortUser.PROCESS_IMPORT else _t("Export Error")
            with wx.MessageDialog(
                    self,
                    _t("The following error was generated") +
                    f"\n\n{data}\n\n" +
                    _t("Be aware that already processed fits were not saved"),
                    _message, wx.OK | wx.ICON_ERROR
            ) as dlg:
                dlg.ShowModal()
            return

        # data is str
        if action & IPortUser.PROCESS_IMPORT:
            if action & IPortUser.ID_PULSE:
                _message = ()
            # update message
            elif action & IPortUser.ID_UPDATE:  # and data != self.progressDialog.message:
                _message = data

            if _message is not None:
                self.__progress_flag, _unuse = self.progressDialog.Pulse(_message)
            else:
                self.closeProgressDialog()
                if action & IPortUser.ID_DONE:
                    self._openAfterImport(data)
        # data is tuple(int, str)
        elif action & IPortUser.PROCESS_EXPORT:
            if action & IPortUser.ID_DONE:
                self.closeProgressDialog()
            else:
                self.__progress_flag, _unuse = self.progressDialog.Update(data[0], data[1])

    def _openAfterImport(self, fits):
        if len(fits) > 0:
            if len(fits) == 1:
                fit = fits[0]
                wx.PostEvent(self, FitSelected(fitID=fit.ID, from_import=True))
                wx.PostEvent(self.shipBrowser, Stage3Selected(shipID=fit.shipID, back=True))
            else:
                fits.sort(key=lambda _fit: (_fit.ship.item.name, _fit.name))
                results = []
                for fit in fits:
                    results.append((
                        fit.ID,
                        fit.name,
                        fit.modifiedCoalesce,
                        fit.ship.item,
                        fit.notes
                    ))
                wx.PostEvent(self.shipBrowser, ImportSelected(fits=results, back=True))

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
        with wx.FileDialog(
                self,
                _t("Open One Or More Character Files"),
                wildcard="|".join([
                    _t("EVE API XML character files") + " (*.xml)|*.xml",
                    _t("All Files") + "|*"
                ]),
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.supress_left_up = True
                self.waitDialog = wx.BusyInfo(_t("Importing Character..."), parent=self)
                sCharacter = Character.getInstance()
                sCharacter.importCharacter(dlg.GetPaths(), self.importCharacterCallback)

    def importCharacterCallback(self):
        self.closeWaitDialog()
        wx.PostEvent(self, GE.CharListUpdated())

    def closeWaitDialog(self):
        del self.waitDialog

    def openWXInspectTool(self, event):
        if not InspectionTool().initialized:
            InspectionTool().Init()

        # Find a widget to be selected in the tree.  Use either the
        # one under the cursor, if any, or this frame.
        wnd, _ = wx.FindWindowAtPointer()
        if not wnd:
            wnd = self
        InspectionTool().Show(wnd, True)
