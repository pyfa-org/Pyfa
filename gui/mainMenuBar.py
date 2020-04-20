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

import config
import graphs
from service.character import Character
from service.fit import Fit
import gui.globalEvents as GE
from gui.bitmap_loader import BitmapLoader

from logbook import Logger

pyfalog = Logger(__name__)


class MainMenuBar(wx.MenuBar):
    def __init__(self, mainFrame):
        pyfalog.debug("Initialize MainMenuBar")
        self.characterEditorId = wx.NewId()
        self.damagePatternEditorId = wx.NewId()
        self.targetProfileEditorId = wx.NewId()
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
        self.toggleIgnoreRestrictionID = wx.NewId()
        self.devToolsId = wx.NewId()
        self.optimizeFitPrice = wx.NewId()

        self.mainFrame = mainFrame
        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        self.Append(fileMenu, "&File")

        fileMenu.Append(self.mainFrame.addPageId, "&New Tab\tCTRL+T", "Open a new fitting tab")
        fileMenu.Append(self.mainFrame.closePageId, "&Close Tab\tCTRL+W", "Close the current fit")
        fileMenu.Append(self.mainFrame.closeAllPagesId, "&Close All Tabs\tCTRL+ALT+W", "Close all open fits")

        fileMenu.AppendSeparator()
        fileMenu.Append(self.backupFitsId, "&Backup All Fittings", "Backup all fittings to a XML file")
        fileMenu.Append(self.exportHtmlId, "Export All Fittings to &HTML", "Export fits to HTML file (set in Preferences)")

        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_EXIT)

        # Fit menu
        fitMenu = wx.Menu()
        self.Append(fitMenu, "Fi&t")

        fitMenu.Append(wx.ID_UNDO, "&Undo\tCTRL+Z", "Undo the most recent action")
        fitMenu.Append(wx.ID_REDO, "&Redo\tCTRL+Y", "Redo the most recent undone action")

        fitMenu.AppendSeparator()
        fitMenu.Append(wx.ID_COPY, "&To Clipboard\tCTRL+C", "Export a fit to the clipboard")
        fitMenu.Append(wx.ID_PASTE, "&From Clipboard\tCTRL+V", "Import a fit from the clipboard")

        fitMenu.AppendSeparator()
        fitMenu.Append(wx.ID_OPEN, "&Import Fittings\tCTRL+O", "Import fittings into pyfa")
        fitMenu.Append(wx.ID_SAVEAS, "&Export Fitting\tCTRL+S", "Export fitting to another format")

        fitMenu.AppendSeparator()
        fitMenu.Append(self.optimizeFitPrice, "&Optimize Fit Price\tCTRL+D")
        graphFrameItem = wx.MenuItem(fitMenu, self.graphFrameId, "&Graphs\tCTRL+G")
        graphFrameItem.SetBitmap(BitmapLoader.getBitmap("graphs_small", "gui"))
        fitMenu.Append(graphFrameItem)
        if not graphs.graphFrame_enabled:
            self.Enable(self.graphFrameId, False)
        self.ignoreRestrictionItem = fitMenu.Append(self.toggleIgnoreRestrictionID, "Disable Fitting Re&strictions")

        fitMenu.AppendSeparator()
        fitMenu.Append(self.eveFittingsId, "&Browse ESI Fittings\tCTRL+B")
        fitMenu.Append(self.exportToEveId, "E&xport to ESI\tCTRL+E")
        self.Enable(self.eveFittingsId, True)
        self.Enable(self.exportToEveId, True)

        # Character menu
        characterMenu = wx.Menu()
        self.Append(characterMenu, "&Character")

        characterMenu.Append(self.saveCharId, "&Save Character")
        characterMenu.Append(self.saveCharAsId, "Save Character &As...")
        characterMenu.Append(self.revertCharId, "&Revert Character")

        characterMenu.AppendSeparator()
        characterMenu.Append(self.importCharacterId, "&Import Character File", "Import characters into pyfa from file")
        characterMenu.Append(self.exportSkillsNeededId, "&Export Skills Needed", "Export skills needed for this fitting")

        characterMenu.AppendSeparator()
        characterMenu.Append(self.ssoLoginId, "&Manage ESI Characters")

        # Global Menu
        globalMenu = wx.Menu()

        if not self.mainFrame.disableOverrideEditor:
            attrItem = wx.MenuItem(globalMenu, self.attrEditorId, "Attribute &Overrides")
            attrItem.SetBitmap(BitmapLoader.getBitmap("fit_rename_small", "gui"))
            globalMenu.Append(attrItem)
            globalMenu.Append(self.toggleOverridesId, "&Turn Overrides On")
            globalMenu.AppendSeparator()


        self.Append(globalMenu, "&Global")
        preferencesShortCut = "CTRL+," if 'wxMac' in wx.PlatformInfo else "CTRL+P"
        preferencesItem = wx.MenuItem(globalMenu, wx.ID_PREFERENCES, "&Preferences\t" + preferencesShortCut)
        preferencesItem.SetBitmap(BitmapLoader.getBitmap("preferences_small", "gui"))
        globalMenu.Append(preferencesItem)

        # Editors menu
        editorsMenu = wx.Menu()
        self.Append(editorsMenu, "&Editors")
        charEditItem = wx.MenuItem(editorsMenu, self.characterEditorId, "&Character Editor\tCTRL+K")
        charEditItem.SetBitmap(BitmapLoader.getBitmap("character_small", "gui"))
        editorsMenu.Append(charEditItem)
        implantSetEditItem = wx.MenuItem(editorsMenu, self.implantSetEditorId, "&Implant Set Editor\tCTRL+I")
        implantSetEditItem.SetBitmap(BitmapLoader.getBitmap("hardwire_small", "gui"))
        editorsMenu.Append(implantSetEditItem)
        damagePatternEditItem = wx.MenuItem(editorsMenu, self.damagePatternEditorId, "&Damage Pattern Editor")
        damagePatternEditItem.SetBitmap(BitmapLoader.getBitmap("damagePattern_small", "gui"))
        editorsMenu.Append(damagePatternEditItem)
        targetProfileEditItem = wx.MenuItem(editorsMenu, self.targetProfileEditorId, "&Target Profile Editor")
        targetProfileEditItem.SetBitmap(BitmapLoader.getBitmap("explosive_small", "gui"))
        editorsMenu.Append(targetProfileEditItem)

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, "&Help")
        helpMenu.Append(self.wikiId, "&Wiki", "Go to wiki on GitHub")
        helpMenu.Append(self.forumId, "&Forums", "Go to EVE Online Forum thread")
        helpMenu.AppendSeparator()
        helpMenu.Append(wx.ID_ABOUT)

        if config.debug:
            helpMenu.Append(self.mainFrame.widgetInspectMenuID, "Open Wid&gets Inspect tool", "Open Widgets Inspect tool")
            helpMenu.Append(self.devToolsId, "Open &Dev Tools", "Dev Tools")

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(GE.FIT_RENAMED, self.fitRenamed)

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return
        enable = activeFitID is not None
        self.Enable(wx.ID_SAVEAS, enable)
        self.Enable(wx.ID_COPY, enable)
        self.Enable(self.exportSkillsNeededId, enable)

        self.refreshUndo()

        sChar = Character.getInstance()
        charID = self.mainFrame.charSelection.getActiveCharacter()
        char = sChar.getCharacter(charID)

        # enable/disable character saving stuff
        self.Enable(self.saveCharId, not char.ro and char.isDirty)
        self.Enable(self.saveCharAsId, char.isDirty)
        self.Enable(self.revertCharId, char.isDirty)

        self.Enable(self.toggleIgnoreRestrictionID, enable)

        if activeFitID:
            sFit = Fit.getInstance()
            fit = sFit.getFit(activeFitID)

            if fit.ignoreRestrictions:
                self.ignoreRestrictionItem.SetItemLabel("Enable Fitting Re&strictions")
            else:
                self.ignoreRestrictionItem.SetItemLabel("Disable Fitting Re&strictions")

    def fitRenamed(self, event):
        self.refreshUndo()
        event.Skip()

    def refreshUndo(self):
        command = self.mainFrame.command
        self.Enable(wx.ID_UNDO, False)
        self.Enable(wx.ID_REDO, False)
        if command.CanUndo():
            self.Enable(wx.ID_UNDO, True)
        if command.CanRedo():
            self.Enable(wx.ID_REDO, True)
