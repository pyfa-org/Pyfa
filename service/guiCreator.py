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
#from gui.statsView import StatsView
from gui import builtinStatsViews
from gui.bitmapLoader import BitmapLoader
from gui import pygauge as PG
import gui.mainFrame
import gui.chromeTabs

from eos.types import Hardpoint

from gui.utils.numberFormatter import formatAmount

class guiCreator():

    def createColumns(self, contentPanel, headerPanel, guiInfo):

        # guiInfo format
        # ["Text","Label","Column","Bitmap","Tooltip","Suffix"]

        contentSizer = contentPanel.GetSizer()
        root = wx.BoxSizer(wx.VERTICAL)
        contentSizer.Add(root, 0, wx.EXPAND, 0)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(sizer, 0, wx.EXPAND)
        root.Add(wx.StaticLine(contentPanel, wx.ID_ANY, style=wx.HORIZONTAL), 0, wx.EXPAND)

        sizerResources = wx.BoxSizer(wx.HORIZONTAL)
        root.Add(sizerResources, 1, wx.EXPAND, 0)

        parent = self.panel = contentPanel
        self.headerPanel = headerPanel
        panel = "full"


        base = sizerResources

        for i, group in enumerate((("drones", "droneBandwidth", "droneBay"), ("fighter", "fighterBay"))):
            main = wx.BoxSizer(wx.VERTICAL)
            base.Add(main, 1, wx.ALIGN_CENTER)

            for type in group:
                capitalizedType = type[0].capitalize() + type[1:]
                bitmap = BitmapLoader.getStaticBitmap(type + "_big", parent, "gui")
                #tooltip = wx.ToolTip(tooltipText[type])
                #bitmap.SetToolTip(tooltip)

                stats = wx.BoxSizer(wx.VERTICAL)
                absolute = wx.BoxSizer(wx.HORIZONTAL)
                stats.Add(absolute, 0, wx.EXPAND)

                b = wx.BoxSizer(wx.HORIZONTAL)
                main.Add(b, 1, wx.ALIGN_CENTER)

                b.Add(bitmap, 0, wx.ALIGN_BOTTOM)

                b.Add(stats, 1, wx.EXPAND)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                test = ("label%sUsed%s" % (panel.capitalize(), capitalizedType), lbl)
                setattr(self, "label%sUsed%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT | wx.LEFT, 3)

                absolute.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sTotal%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "%s" % units[type])
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                # Gauges modif. - Darriele

                gauge = PG.PyGauge(parent, wx.ID_ANY, 1)
                gauge.SetValueRange(0, 0)
                gauge.SetMinSize((self.getTextExtentW("1.999M/1.99M MW"), 23))
                gauge.SetFractionDigits(2)

                setattr(self, "gauge%s%s" % (panel.capitalize(), capitalizedType), gauge)
                stats.Add(gauge, 0, wx.ALIGN_CENTER)

                setattr(self, "base%s%s" % (panel.capitalize(), capitalizedType), b)
                setattr(self, "bitmap%s%s" % (panel.capitalize(), capitalizedType), bitmap)

        return contentSizer