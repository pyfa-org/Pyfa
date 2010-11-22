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
import bitmapLoader
import gui.mainFrame
import gui.graphFrame

class MainMenuBar(wx.MenuBar):
    def __init__(self):
        self.characterEditorId = wx.NewId()
        self.damagePatternEditorId = wx.NewId()
        self.graphFrameId = wx.NewId()
        self.backupFitsId = wx.NewId()

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        self.Append(fileMenu, "&File")

        fileMenu.Append(self.mainFrame.addPageId, "&New Tab\tCTRL+T", "Open a new fitting tab")
        fileMenu.Append(self.mainFrame.closePageId, "&Close Tab\tCTRL+W", "Close the current fit")
        fileMenu.AppendSeparator()

        fileMenu.Append(self.backupFitsId, "&Backup fits", "Backup all fittings to a XML file")
        fileMenu.Append(wx.ID_OPEN, "&Import\tCTRL+O", "Import a fit into pyfa.")
        fileMenu.Append(wx.ID_SAVEAS, "&Export\tCTRL+S", "Export the fit to another format.")
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
        graphFrameItem.Enable(gui.graphFrame.enabled)
        windowMenu.AppendItem(graphFrameItem)

        #windowMenu.Append(wx.ID_PREFERENCES)

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, "&Help")
        helpMenu.Append(wx.ID_ABOUT)
        #helpMenu.Append(wx.ID_HELP, "User manual", "User manual")
        helpMenu.Append(911,"Open Widgets Inspect tool", "Open Widgets Inspect tool")



        self.mainFrame.Bind(gui.builtinViews.fittingView.FIT_CHANGED, self.fitChanged)

    def fitChanged(self, event):
        enable = event.fitID is not None
        self.Enable(wx.ID_SAVEAS, enable)
        self.Enable(wx.ID_COPY, enable)
        event.Skip()

