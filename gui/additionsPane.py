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

from gui.bitmap_loader import BitmapLoader
from gui.builtinAdditionPanes.boosterView import BoosterView
from gui.builtinAdditionPanes.cargoView import CargoView
from gui.builtinAdditionPanes.commandView import CommandView
from gui.builtinAdditionPanes.droneView import DroneView
from gui.builtinAdditionPanes.fighterView import FighterView
from gui.builtinAdditionPanes.implantView import ImplantView
from gui.builtinAdditionPanes.notesView import NotesView
from gui.builtinAdditionPanes.projectedView import ProjectedView
from gui.chrome_tabs import ChromeNotebook
from gui.toggle_panel import TogglePanel


class AdditionsPane(TogglePanel):
    def __init__(self, parent):

        TogglePanel.__init__(self, parent, force_layout=1)

        self.SetLabel("Additions")
        pane = self.GetContentPanel()

        baseSizer = wx.BoxSizer(wx.HORIZONTAL)
        pane.SetSizer(baseSizer)

        self.notebook = ChromeNotebook(pane, False)
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
        self.notebook.AddPage(self.drone, "Drones", image=droneImg, closeable=False)

        self.fighter = FighterView(self.notebook)
        self.notebook.AddPage(self.fighter, "Fighters", image=fighterImg, closeable=False)

        self.cargo = CargoView(self.notebook)
        self.notebook.AddPage(self.cargo, "Cargo", image=cargoImg, closeable=False)

        self.implant = ImplantView(self.notebook)
        self.notebook.AddPage(self.implant, "Implants", image=implantImg, closeable=False)

        self.booster = BoosterView(self.notebook)
        self.notebook.AddPage(self.booster, "Boosters", image=boosterImg, closeable=False)

        self.projectedPage = ProjectedView(self.notebook)
        self.notebook.AddPage(self.projectedPage, "Projected", image=projectedImg, closeable=False)

        self.gangPage = CommandView(self.notebook)
        self.notebook.AddPage(self.gangPage, "Command", image=gangImg, closeable=False)

        self.notes = NotesView(self.notebook)
        self.notebook.AddPage(self.notes, "Notes", image=notesImg, closeable=False)

        self.notebook.SetSelection(0)

    PANES = ["Drones", "Fighters", "Cargo", "Implants", "Boosters", "Projected", "Command", "Notes"]

    def select(self, name):
        self.notebook.SetSelection(self.PANES.index(name))

    def getName(self, idx):
        return self.PANES[idx]

    def ToggleContent(self, event):
        TogglePanel.ToggleContent(self, event)
        h = self.header_panel.GetSize()[1] + 4

        if self.IsCollapsed():
            self.old_pos = self.parent.GetSashPosition()
            self.parent.SetMinimumPaneSize(h)
            self.parent.SetSashPosition(h * -1, True)
            self.parent.SetSashInvisible(True)
        else:
            self.parent.SetSashInvisible(False)
            self.parent.SetMinimumPaneSize(200)
            self.parent.SetSashPosition(self.old_pos, True)
