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
from gui.bitmap_loader import BitmapLoader
from multilanguage import translate
from multilanguage import packs
from multilanguage import language

from logbook import Logger

# from service.crest import Crest
# from service.crest import CrestModes

pyfalog = Logger(__name__)


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
        self.devToolsId = wx.NewId()
        self.languageId = []

        # pheonix: evaluate if this is needed
        if 'wxMac' in wx.PlatformInfo and wx.VERSION >= (3, 0):
            wx.ID_COPY = wx.NewId()
            wx.ID_PASTE = wx.NewId()

        self.mainFrame = mainFrame
        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        self.Append(fileMenu, translate.look_up("ui", "&File"))

        fileMenu.Append(self.mainFrame.addPageId, translate.look_up("ui", "&New Tab\tCTRL+T"), "Open a new fitting tab")
        fileMenu.Append(self.mainFrame.closePageId, translate.look_up("ui", "&Close Tab\tCTRL+W"),
                        "Close the current fit")
        fileMenu.AppendSeparator()

        fileMenu.Append(self.backupFitsId, translate.look_up("ui", "&Backup All Fittings"),
                        "Backup all fittings to a XML file")
        fileMenu.Append(wx.ID_OPEN, translate.look_up("ui", "&Import Fittings\tCTRL+O"), "Import fittings into pyfa")
        fileMenu.Append(wx.ID_SAVEAS, translate.look_up("ui", "&Export Fitting\tCTRL+S"),
                        "Export fitting to another format")
        fileMenu.AppendSeparator()
        fileMenu.Append(self.exportHtmlId, translate.look_up("ui", "Export HTML"),
                        "Export fits to HTML file (set in Preferences)")
        fileMenu.Append(self.exportSkillsNeededId, translate.look_up("ui", "Export &Skills Needed"),
                        "Export skills needed for this fitting")
        fileMenu.Append(self.importCharacterId, translate.look_up("ui", "Import C&haracter File"),
                        "Import characters into pyfa from file")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_EXIT)

        # Edit menu
        editMenu = wx.Menu()
        self.Append(editMenu, translate.look_up("ui", "&Edit"))

        # editMenu.Append(wx.ID_UNDO)
        # editMenu.Append(wx.ID_REDO)

        editMenu.Append(wx.ID_COPY, translate.look_up("ui", "To Clipboard\tCTRL+C"), "Export a fit to the clipboard")
        editMenu.Append(wx.ID_PASTE, translate.look_up("ui", "From Clipboard\tCTRL+V"),
                        "Import a fit from the clipboard")
        editMenu.AppendSeparator()
        editMenu.Append(self.saveCharId, translate.look_up("ui", "Save Character"))
        editMenu.Append(self.saveCharAsId, translate.look_up("ui", "Save Character As..."))
        editMenu.Append(self.revertCharId, translate.look_up("ui", "Revert Character"))
        editMenu.AppendSeparator()
        self.ignoreRestrictionItem = editMenu.Append(self.toggleIgnoreRestrictionID,
                                                     translate.look_up("ui", "Ignore Fitting Restrictions"))

        # Character menu
        windowMenu = wx.Menu()
        self.Append(windowMenu, translate.look_up("ui", "&Window"))

        charEditItem = wx.MenuItem(windowMenu, self.characterEditorId,
                                   translate.look_up("ui", "&Character Editor\tCTRL+E"))
        charEditItem.SetBitmap(BitmapLoader.getBitmap("character_small", "gui"))
        windowMenu.Append(charEditItem)

        damagePatternEditItem = wx.MenuItem(windowMenu, self.damagePatternEditorId,
                                            translate.look_up("ui", "Damage Pattern Editor\tCTRL+D"))
        damagePatternEditItem.SetBitmap(BitmapLoader.getBitmap("damagePattern_small", "gui"))
        windowMenu.Append(damagePatternEditItem)

        targetResistsEditItem = wx.MenuItem(windowMenu, self.targetResistsEditorId,
                                            translate.look_up("ui", "Target Resists Editor\tCTRL+R"))
        targetResistsEditItem.SetBitmap(BitmapLoader.getBitmap("explosive_small", "gui"))
        windowMenu.Append(targetResistsEditItem)

        implantSetEditItem = wx.MenuItem(windowMenu, self.implantSetEditorId,
                                         translate.look_up("ui", "Implant Set Editor\tCTRL+I"))
        implantSetEditItem.SetBitmap(BitmapLoader.getBitmap("hardwire_small", "gui"))
        windowMenu.Append(implantSetEditItem)

        graphFrameItem = wx.MenuItem(windowMenu, self.graphFrameId, translate.look_up("ui", "Graphs\tCTRL+G"))
        graphFrameItem.SetBitmap(BitmapLoader.getBitmap("graphs_small", "gui"))
        windowMenu.Append(graphFrameItem)

        if not gui.graphFrame.graphFrame_enabled:
            self.Enable(self.graphFrameId, False)

        preferencesShortCut = "CTRL+," if 'wxMac' in wx.PlatformInfo else "CTRL+P"
        preferencesItem = wx.MenuItem(windowMenu, wx.ID_PREFERENCES,
                                      translate.look_up("ui", "Preferences\t") + preferencesShortCut)
        preferencesItem.SetBitmap(BitmapLoader.getBitmap("preferences_small", "gui"))
        windowMenu.Append(preferencesItem)

        # self.sEsi = Crest.getInstance()

        # CREST Menu
        esiMMenu = wx.Menu()
        self.Append(esiMMenu, translate.look_up("ui", "EVE &SSO"))

        esiMMenu.Append(self.ssoLoginId, translate.look_up("ui", "Manage Characters"))
        esiMMenu.Append(self.eveFittingsId, translate.look_up("ui", "Browse EVE Fittings"))
        esiMMenu.Append(self.exportToEveId, translate.look_up("ui", "Export To EVE"))

        # if self.sEsi.settings.get('mode') == CrestModes.IMPLICIT or len(self.sEsi.getCrestCharacters()) == 0:
        self.Enable(self.eveFittingsId, True)
        self.Enable(self.exportToEveId, True)

        if not self.mainFrame.disableOverrideEditor:
            windowMenu.AppendSeparator()
            attrItem = wx.MenuItem(windowMenu, self.attrEditorId,
                                   translate.look_up("ui", "Attribute Overrides\tCTRL+B"))
            attrItem.SetBitmap(BitmapLoader.getBitmap("fit_rename_small", "gui"))
            windowMenu.Append(attrItem)
            windowMenu.Append(self.toggleOverridesId, translate.look_up("ui", "Turn Overrides On"))

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, translate.look_up("ui", "&Help"))
        helpMenu.Append(self.wikiId, translate.look_up("ui", "Wiki"), "Go to wiki on GitHub")
        helpMenu.Append(self.forumId, translate.look_up("ui", "Forums"), "Go to EVE Online Forum thread")
        helpMenu.AppendSeparator()
        helpMenu.Append(self.importDatabaseDefaultsId, translate.look_up("ui", "Import D&atabase Defaults"),
                        "Imports missing database defaults")
        helpMenu.AppendSeparator()
        helpMenu.Append(wx.ID_ABOUT)

        # Language menu
        languageMenu = wx.Menu()
        self.Append(languageMenu, translate.look_up("ui", "&Language"))
        for item in packs.packs_list:
            temp = wx.NewId()
            self.languageId.append(temp)
            languageMenu.Append(temp, translate.look_up("ui", item), item)

        if config.debug:
            helpMenu.Append(self.mainFrame.widgetInspectMenuID, translate.look_up("ui", "Open Widgets Inspect tool"),
                            "Open Widgets Inspect tool")
            helpMenu.Append(self.devToolsId, translate.look_up("ui", "Open Dev Tools"),
                            "Dev Tools")

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
                self.ignoreRestrictionItem.SetItemLabel(translate.look_up("ui", "Enable Fitting Restrictions"))
            else:
                self.ignoreRestrictionItem.SetItemLabel(translate.look_up("ui", "Disable Fitting Restrictions"))

        event.Skip()
