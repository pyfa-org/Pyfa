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
from gui import bitmapLoader

class StatsPane(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        size = wx.Size()
        size.SetWidth(315)
        self.SetMinSize(size)

        self.sizerBase = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizerBase)

        self.sizerHeaderResources = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(self.sizerHeaderResources, 0, wx.EXPAND)

        # Resources header
        self.labelResources = wx.StaticText(self, wx.ID_ANY, "Resources")
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        self.labelResources.SetFont(font)
        self.sizerHeaderResources.Add(self.labelResources, 0, wx.ALIGN_CENTER)
        self.sizerHeaderResources.Add(wx.StaticLine(self, wx.ID_ANY), 1, wx.EXPAND)

        # Resources stuff
        self.sizerResources = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(self.sizerResources)

        # Turret slots, Launcher slots & calibration
        self.sizerHardResources = wx.FlexGridSizer(3, 4)
        self.sizerResources.Add(self.sizerHardResources, 0, wx.ALIGN_CENTER)

        for type in ("turret", "launcher"):
            self.sizerHardResources.Add(bitmapLoader.getStaticBitmap("%s_big" % type, self))

            lbl = wx.StaticText(self, wx.ID_ANY, "0")
            setattr(self, "labelAvailable%sHardpoints", lbl)
            self.sizerHardResources.Add(lbl, 0, wx.ALIGN_CENTER)

            self.sizerHardResources.Add(wx.StaticText(self, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(self, wx.ID_ANY, "0")
            setattr(self, "labelTotal%sHardpoints", lbl)
            self.sizerHardResources.Add(lbl, 0, wx.ALIGN_CENTER)


        # Calibration points
        self.sizerHardResources.Add(bitmapLoader.getStaticBitmap("calibration_big", self))

        self.labelAvailableCalibrationPoints = wx.StaticText(self, wx.ID_ANY, "0")
        self.sizerHardResources.Add(self.labelAvailableCalibrationPoints, 0, wx.ALIGN_CENTER)

        self.sizerHardResources.Add(wx.StaticText(self, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

        self.labelTotalCalibrationPoints = wx.StaticText(self, wx.ID_ANY, "0")
        self.sizerHardResources.Add(self.labelTotalCalibrationPoints, 0, wx.ALIGN_CENTER)

        self.sizerResources.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.VERTICAL), 1, wx.EXPAND)

        #PG, Cpu & drone stuff
        for group in (("cpu", "pg"), ("droneBay", "droneBandwidth")):
            main = wx.BoxSizer(wx.VERTICAL)
            self.sizerResources.Add(main, 0, wx.EXPAND)
            for type in group:
                capitalizedType = type[0].capitalize() + type[1:]

                base = wx.BoxSizer(wx.HORIZONTAL)
                main.Add(base, 0, wx.EXPAND)

                base.Add(bitmapLoader.getStaticBitmap(type + "_big", self), 0, wx.ALIGN_CENTER)

                stats = wx.BoxSizer(wx.VERTICAL)
                base.Add(stats, 0, wx.EXPAND)

                absolute =  wx.BoxSizer(wx.HORIZONTAL)
                stats.Add(absolute)

                lbl = wx.StaticText(self, wx.ID_ANY, "0")
                setattr(self, "labelAvailable%s" % capitalizedType, lbl)
                absolute.Add(lbl, 0, wx.ALIGN_CENTER)

                absolute.Add(wx.StaticText(self, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

                lbl = wx.StaticText(self, wx.ID_ANY, "0")
                setattr(self, "labelTotal%s" % capitalizedType, lbl)
                absolute.Add(lbl, 0, wx.ALIGN_CENTER)

                gauge = wx.Gauge(self, wx.ID_ANY, 100)
                setattr(self, "gauge%s" % capitalizedType, gauge)
                stats.Add(gauge)

            if "cpu" in group:
                self.sizerResources.Add(wx.StaticLine(self, wx.ID_ANY, style=wx.VERTICAL), 1, wx.EXPAND)

        # Resistances
        self.sizerHeaderResistances = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerBase.Add(self.sizerHeaderResistances, 0, wx.EXPAND)

        # Header & EHP
        self.labelResistances = wx.StaticText(self, wx.ID_ANY, "Resistances")
        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        self.labelResistances.SetFont(font)
        self.sizerHeaderResistances.Add(self.labelResistances, 0, wx.ALIGN_CENTER)

        self.labelEhpHeader = wx.StaticText(self, wx.ID_ANY, " (Effective HP: ")
        self.sizerHeaderResistances.Add(self.labelEhpHeader, 0, wx.ALIGN_CENTER)

        self.labelEhp = wx.StaticText(self, wx.ID_ANY, "0")
        self.sizerHeaderResistances.Add(self.labelEhp, 0, wx.ALIGN_CENTER)

        self.labelEhpHeader = wx.StaticText(self, wx.ID_ANY, ")")
        self.sizerHeaderResistances.Add(self.labelEhpHeader, 0, wx.ALIGN_CENTER)

        self.sizerHeaderResistances.Add(wx.StaticLine(self, wx.ID_ANY), 1, wx.EXPAND)
