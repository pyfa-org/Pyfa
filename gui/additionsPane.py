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

from gui.bitmapLoader import BitmapLoader
from gui.builtinAdditionPanes.boosterView import BoosterView
from gui.builtinAdditionPanes.cargoView import CargoView
from gui.builtinAdditionPanes.commandView import CommandView
from gui.builtinAdditionPanes.droneView import DroneView
from gui.builtinAdditionPanes.fighterView import FighterView
from gui.builtinAdditionPanes.implantView import ImplantView
from gui.builtinAdditionPanes.notesView import NotesView
from gui.builtinAdditionPanes.projectedView import ProjectedView
from gui.chromeTabs import PFNotebook
from gui.pyfatogglepanel import TogglePanel


class AdditionsPane(TogglePanel):
    def __init__(self, parent):

        TogglePanel.__init__(self, parent, forceLayout=1)

        self.SetLabel("Additions")
        pane = self.GetContentPane()

        baseSizer = wx.BoxSizer(wx.HORIZONTAL)
        pane.SetSizer(baseSizer)

        self.notebook = PFNotebook(pane, False)
        self.notebook.SetMinSize((-1, 1000))

        baseSizer.Add(self.notebook, 1, wx.EXPAND)

        droneImg = BitmapLoader.getImage("drone_small", "gui")
        fighterImg = BitmapLoader.getImage("fighter_small", "gui")
        implantImg = BitmapLoader.getImage("implant_small", "gui")
        boosterImg = BitmapLoader.getImage("booster_small", "gui")
        projectedImg = BitmapLoader.getImage("projected_small", "gui")
        gangImg = BitmapLoader.getImage("fleet_fc_small", "gui")
        cargoImg = BitmapLoader.getImage("cargo_small", "gui")
        notesImg = BitmapLoader.getImage("skill_small", "gui")

        self.drone = DroneView(self.notebook)
        self.notebook.AddPage(self.drone, "Drones", tabImage=droneImg, showClose=False)

        self.fighter = FighterView(self.notebook)
        self.notebook.AddPage(self.fighter, "Fighters", tabImage=fighterImg, showClose=False)

        self.cargo = CargoView(self.notebook)
        self.notebook.AddPage(self.cargo, "Cargo", tabImage=cargoImg, showClose=False)

        self.implant = ImplantView(self.notebook)
        self.notebook.AddPage(self.implant, "Implants", tabImage=implantImg, showClose=False)

        self.booster = BoosterView(self.notebook)
        self.notebook.AddPage(self.booster, "Boosters", tabImage=boosterImg, showClose=False)

        self.projectedPage = ProjectedView(self.notebook)
        self.notebook.AddPage(self.projectedPage, "Projected", tabImage=projectedImg, showClose=False)

        self.gangPage = CommandView(self.notebook)
        self.notebook.AddPage(self.gangPage, "Command", tabImage=gangImg, showClose=False)

        self.notes = NotesView(self.notebook)
        self.notebook.AddPage(self.notes, "Notes", tabImage=notesImg, showClose=False)

        self.notebook.SetSelection(0)

    PANES = ["Drones", "Fighters", "Cargo", "Implants", "Boosters", "Projected", "Command", "Notes"]

    def select(self, name):
        self.notebook.SetSelection(self.PANES.index(name))

    def getName(self, idx):
        return self.PANES[idx]

    def toggleContent(self, event):
        TogglePanel.toggleContent(self, event)
        h = self.headerPanel.GetSize()[1] + 4

        if self.IsCollapsed():
            self.old_pos = self.parent.GetSashPosition()
            self.parent.SetMinimumPaneSize(h)
            self.parent.SetSashPosition(h * -1, True)
            # only available in >= wx2.9
            if getattr(self.parent, "SetSashInvisible", None):
                self.parent.SetSashInvisible(True)
        else:
            if getattr(self.parent, "SetSashInvisible", None):
                self.parent.SetSashInvisible(False)
            self.parent.SetMinimumPaneSize(200)
            self.parent.SetSashPosition(self.old_pos, True)
