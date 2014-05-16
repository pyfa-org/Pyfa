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
import config
import bitmapLoader
import gui.mainFrame
import gui.graphFrame
import gui.globalEvents as GE

class MainMenuBar(wx.MenuBar):
    def __init__(self):
        self.characterEditorId = wx.NewId()
        self.damagePatternEditorId = wx.NewId()
        self.graphFrameId = wx.NewId()
        self.backupFitsId = wx.NewId()
        self.exportSkillsNeededId = wx.NewId()
        self.importCharacterId = wx.NewId()
        self.exportHtmlId = wx.NewId()
        self.wikiId = wx.NewId()
        self.forumId = wx.NewId()

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

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

        #editMenu.Append(wx.ID_UNDO)
        #editMenu.Append(wx.ID_REDO)

        copyText = "&To Clipboard" + ("\tCTRL+C" if 'wxMSW' in wx.PlatformInfo else "")
        pasteText = "&From Clipboard" + ("\tCTRL+V" if 'wxMSW' in wx.PlatformInfo else "")
        editMenu.Append(wx.ID_COPY, copyText, "Export a fit to the clipboard")
        editMenu.Append(wx.ID_PASTE, pasteText, "Import a fit from the clipboard")

        # Character menu
        windowMenu = wx.Menu()
        self.Append(windowMenu, "&Window")

        charEditItem = wx.MenuItem(windowMenu, self.characterEditorId, "&Character Editor\tCTRL+E")
        charEditItem.SetBitmap(bitmapLoader.getBitmap("character_small", "icons"))
        windowMenu.AppendItem(charEditItem)

        damagePatternEditItem = wx.MenuItem(windowMenu, self.damagePatternEditorId, "Damage Pattern Editor\tCTRL+D")
        damagePatternEditItem.SetBitmap(bitmapLoader.getBitmap("damagePattern_small", "icons"))
        windowMenu.AppendItem(damagePatternEditItem)

        graphFrameItem = wx.MenuItem(windowMenu, self.graphFrameId, "Graphs\tCTRL+G")
        graphFrameItem.SetBitmap(bitmapLoader.getBitmap("graphs_small", "icons"))
        windowMenu.AppendItem(graphFrameItem)

        preferencesItem = wx.MenuItem(windowMenu, wx.ID_PREFERENCES, "Preferences\tCTRL+P")
        preferencesItem.SetBitmap(bitmapLoader.getBitmap("preferences_small", "icons"))
        windowMenu.AppendItem(preferencesItem)

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, "&Help")
        helpMenu.Append(self.wikiId, "Wiki", "Go to wiki on GitHub")
        helpMenu.Append(self.forumId, "Forums", "Go to EVE Online Forum thread")
        helpMenu.AppendSeparator()
        helpMenu.Append(wx.ID_ABOUT)

        if config.debug:
            helpMenu.Append( self.mainFrame.widgetInspectMenuID, "Open Widgets Inspect tool", "Open Widgets Inspect tool")

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    def fitChanged(self, event):
        enable = event.fitID is not None
        self.Enable(wx.ID_SAVEAS, enable)
        self.Enable(wx.ID_COPY, enable)
        self.Enable(self.exportSkillsNeededId, enable)
        event.Skip()

