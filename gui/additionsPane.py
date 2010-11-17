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
import gui.mainFrame
from gui.boosterView import BoosterView
from gui.droneView import DroneView
from gui.implantView import ImplantView
from gui.projectedView import ProjectedView
from gui.pyfatogglepanel import TogglePanel
import gui.chromeTabs

class AdditionsPane(TogglePanel):

    def __init__(self, parent):

        TogglePanel.__init__(self, parent, forceLayout = 1)

        self.SetLabel("Additions")
        pane = self.GetContentPane()

        baseSizer = wx.BoxSizer(wx.HORIZONTAL)
        pane.SetSizer(baseSizer)

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

#        self.notebook = wx.Notebook(pane)
        self.notebook = gui.chromeTabs.PFNotebook(pane, False)
        size = wx.Size()
        size.SetHeight(200)
        self.notebook.SetMinSize(size)
        baseSizer.Add(self.notebook, 1, wx.EXPAND)
        self.notebook.AddPage(DroneView(self.notebook), "Drones", showClose = False)
        self.notebook.AddPage(ImplantView(self.notebook), "Implants", showClose = False)
        self.notebook.AddPage(BoosterView(self.notebook), "Boosters", showClose = False)

        self.projectedPage = ProjectedView(self.notebook)
        self.notebook.AddPage(self.projectedPage, "Projected", showClose = False)


    PANES = ["Drones", "Implants", "Boosters"]
    def select(self, name):
        self.notebook.SetSelection(self.PANES.index(name))
