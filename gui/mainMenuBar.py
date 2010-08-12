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

class MainMenuBar(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        self.Append(fileMenu, "&File")

        fileMenu.Append(wx.ID_OPEN, "&Import", "Import a fit into pyfa.")
        fileMenu.Append(wx.ID_SAVEAS, "&Export", "Export the fit to another format.")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program.")


        # Edit menu
        editMenu = wx.Menu()
        self.Append(editMenu, "&Edit")

        editMenu.Append(wx.ID_UNDO, "&Undo", "Undo the last action on this fit.")
        editMenu.Append(wx.ID_REDO, "&Redo", "Redo the last undone action.")
        editMenu.Append(wx.ID_UNDELETE, "Un&delete", "Recover the last deleted fit, if any.")

        # Fit menu
        fitMenu = wx.Menu()
        self.Append(fitMenu, "F&it")

        fitMenu.Append(wx.ID_NEW, "&New", "Create a new fit.").GetBitmap()
        fitMenu.Append(wx.ID_EDIT, "&Rename", "Rename this fit.").GetBitmap()
        fitMenu.Append(wx.ID_COPY, "&Copy", "Copy this fit.").GetBitmap()
        fitMenu.Append(wx.ID_DELETE, "&Delete", "Delete this fit.").GetBitmap()

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, "&Help")
        helpMenu.Append(wx.ID_ABOUT, "&About", "About this program")
        helpMenu.Append(wx.ID_HELP, "User manual", "User manual")
