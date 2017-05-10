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
from service.character import Character
from service.fit import Fit
import gui.graphFrame
import gui.globalEvents as GE
from gui.bitmapLoader import BitmapLoader

from logbook import Logger
pyfalog = Logger(__name__)

if 'wxMac' not in wx.PlatformInfo or ('wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0)):
    from service.crest import Crest
    from service.crest import CrestModes


class MainMenuBar(wx.MenuBar):
    def __init__(self, mainFrame):
        pyfalog.debug("Initialize MainMenuBar")
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
        self.toggleIgnoreRestrictionID = wx.NewId()

        if 'wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0):
            wx.ID_COPY = wx.NewId()
            wx.ID_PASTE = wx.NewId()

        self.mainFrame = mainFrame
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
        editMenu.AppendSeparator()
        self.ignoreRestrictionItem = editMenu.Append(self.toggleIgnoreRestrictionID, "Ignore Fitting Restrictions")

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

        if not gui.graphFrame.graphFrame_enabled:
            self.Enable(self.graphFrameId, False)

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

            if not self.mainFrame.disableOverrideEditor:
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

        self.Enable(self.toggleIgnoreRestrictionID, enable)

        if event.fitID:
            sFit = Fit.getInstance()
            fit = sFit.getFit(event.fitID)

            if fit.ignoreRestrictions:
                self.ignoreRestrictionItem.SetItemLabel("Enable Fitting Restrictions")
            else:
                self.ignoreRestrictionItem.SetItemLabel("Disable Fitting Restrictions")

        event.Skip()
