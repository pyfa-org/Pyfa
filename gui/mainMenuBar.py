#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import wx
import bitmapLoader

class MainMenuBar(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        self.Append(fileMenu, "&File")
        fileMenu.Append(wx.ID_EXIT)


        # Edit menu
        editMenu = wx.Menu()
        self.Append(editMenu, "&Edit")

        editMenu.Append(wx.ID_UNDO)
        editMenu.Append(wx.ID_REDO)

        # Fit menu
        fitMenu = wx.Menu()
        self.Append(fitMenu, "F&it")
        fitMenu.Append(wx.ID_EDIT, "&Rename", "Rename this fit.")
        fitMenu.Append(wx.ID_COPY)
        fitMenu.Append(wx.ID_DELETE)
        fitMenu.Append(wx.ID_UNDELETE)
        fitMenu.AppendSeparator()
        fitMenu.Append(wx.ID_OPEN, "&Import", "Import a fit into pyfa.")
        fitMenu.Append(wx.ID_SAVEAS, "&Export", "Export the fit to another format.")

        # Character menu
        charMenu = wx.Menu()
        self.Append(charMenu, "&Character")

        charEditItem = wx.MenuItem(charMenu, 20, "Character &Editor")
        charEditItem.SetBitmap(bitmapLoader.getBitmap("character_small", "icons"))
        charMenu.AppendItem(charEditItem)

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, "&Help")
        helpMenu.Append(wx.ID_ABOUT)
        helpMenu.Append(wx.ID_HELP, "User manual", "User manual")
