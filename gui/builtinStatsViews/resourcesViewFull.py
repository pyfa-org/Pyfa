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
from gui.statsView import StatsView
from gui import builtinStatsViews
from gui import bitmapLoader
from gui import pygauge as PG

from eos.types import Hardpoint

from util import formatAmount

class ResourcesViewFull(StatsView):
    name = "resourcesViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
    def getHeaderText(self, fit):
        return "Resources"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):

        contentSizer = contentPanel.GetSizer()
        sizerResources = wx.BoxSizer(wx.HORIZONTAL)
        contentSizer.Add( sizerResources, 0, wx.EXPAND, 0)

        parent = self.panel = contentPanel
        self.headerPanel = headerPanel
        panel = "full"

        sizer = wx.FlexGridSizer(3, 2)
        sizer.SetMinSize(wx.Size(27 + self.getTextExtentW("400/400"), 0))
        for i in xrange(3):
            sizer.AddGrowableCol(i + 1)

        base = sizerResources
        base.Add(sizer, 0, wx.ALIGN_CENTER)

        #Turrets & launcher hardslots display
        tooltipText = {"turret":"Turret hardpoints", "launcher":"Launcher hardpoints", "drones":"Drones active", "calibration":"Calibration"}
        for type in ("turret", "launcher", "drones", "calibration"):
            bitmap = bitmapLoader.getStaticBitmap("%s_big" % type, parent, "icons")
            tooltip = wx.ToolTip(tooltipText[type])
            bitmap.SetToolTip(tooltip)
            box = wx.BoxSizer(wx.HORIZONTAL)

            sizer.Add(bitmap, 0, wx.ALIGN_CENTER)
            sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL)

            suffix = {'turret':'Hardpoints', 'launcher':'Hardpoints', 'drones':'Active', 'calibration':'Points'}
            lbl = wx.StaticText(parent, wx.ID_ANY, "0")
            setattr(self, "label%sUsed%s%s" % (panel.capitalize(), type.capitalize(), suffix[type].capitalize()), lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            box.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0")
            setattr(self, "label%sTotal%s%s" % (panel.capitalize(), type.capitalize(), suffix[type].capitalize()), lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

        base.Add(wx.StaticLine(parent, wx.ID_ANY, style=wx.VERTICAL), 0, wx.EXPAND | wx.LEFT, 3 if panel == "full" else 0)

        #PG, Cpu & drone stuff
        tooltipText = {"cpu":"CPU", "pg":"PowerGrid", "droneBay":"Drone bay", "droneBandwidth":"Drone bandwidth"}
        for i, group in enumerate((("cpu", "pg"), ("droneBay", "droneBandwidth"))):
            main = wx.BoxSizer(wx.VERTICAL)
            base.Add(main, 1 , wx.ALIGN_CENTER)

            for type in group:
                capitalizedType = type[0].capitalize() + type[1:]
                bitmap = bitmapLoader.getStaticBitmap(type + "_big", parent, "icons")
                tooltip = wx.ToolTip(tooltipText[type])
                bitmap.SetToolTip(tooltip)

                stats = wx.BoxSizer(wx.VERTICAL)
                absolute =  wx.BoxSizer(wx.HORIZONTAL)
                stats.Add(absolute, 0, wx.EXPAND)

                b = wx.BoxSizer(wx.HORIZONTAL)
                main.Add(b, 1, wx.ALIGN_CENTER)

                b.Add(bitmap, 0, wx.ALIGN_BOTTOM)

                b.Add(stats, 1, wx.EXPAND)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sUsed%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                absolute.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_LEFT)

                lbl = wx.StaticText(parent, wx.ID_ANY, "0")
                setattr(self, "label%sTotal%s" % (panel.capitalize(), capitalizedType), lbl)
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                units = {"cpu":" tf", "pg":" MW", "droneBandwidth":" mbit/s", "droneBay":u" m\u00B3"}
                lbl = wx.StaticText(parent, wx.ID_ANY, "%s" % units[type])
                absolute.Add(lbl, 0, wx.ALIGN_LEFT)

                # Gauges modif. - Darriele

                gauge = PG.PyGauge(parent, wx.ID_ANY, 1)
                gauge.SetValueRange(0, 0)
                gauge.SetMinSize((self.getTextExtentW("1.999M/1.99M MW"), 23))
                gauge.SetFractionDigits(2)

                setattr(self, "gauge%s%s" % (panel.capitalize(),capitalizedType), gauge)
                stats.Add(gauge, 0, wx.ALIGN_CENTER)

    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("label%sUsedTurretHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.TURRET), 0, 0, 0),
                         ("label%sTotalTurretHardpoints", lambda: fit.ship.getModifiedItemAttr('turretSlotsLeft'), 0, 0, 0),
                         ("label%sUsedLauncherHardpoints", lambda: fit.getHardpointsUsed(Hardpoint.MISSILE), 0, 0, 0),
                         ("label%sTotalLauncherHardpoints", lambda: fit.ship.getModifiedItemAttr('launcherSlotsLeft'), 0, 0, 0),
                         ("label%sUsedDronesActive", lambda: fit.usedDronesActive, 0, 0, 0),
                         ("label%sTotalDronesActive", lambda: fit.ship.totalDronesActive, 0, 0, 0),
                         ("label%sUsedCalibrationPoints", lambda: fit.calibrationUsed, 0, 0, 0),
                         ("label%sTotalCalibrationPoints", lambda: fit.ship.getModifiedItemAttr('upgradeCapacity'), 0, 0, 0),
                         ("label%sUsedPg", lambda: fit.pgUsed, 4, 0, 9),
                         ("label%sUsedCpu", lambda: fit.cpuUsed, 4, 0, 9),
                         ("label%sTotalPg", lambda: fit.ship.getModifiedItemAttr("powerOutput"), 4, 0, 9),
                         ("label%sTotalCpu", lambda: fit.ship.getModifiedItemAttr("cpuOutput"), 4, 0, 9),
                         ("label%sUsedDroneBay", lambda: fit.droneBayUsed, 3, 0, 9),
                         ("label%sUsedDroneBandwidth", lambda: fit.droneBandwidthUsed, 3, 0, 9),
                         ("label%sTotalDroneBay", lambda: fit.ship.getModifiedItemAttr("droneCapacity"), 3, 0, 9),
                         ("label%sTotalDroneBandwidth", lambda: fit.ship.getModifiedItemAttr("droneBandwidth"), 3, 0, 9))
        panel = "Full"
        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName % panel)
            value = value() if fit is not None else 0
            value = value if value is not None else 0
            if isinstance(value, basestring):
                label.SetLabel(value)
                label.SetToolTip(wx.ToolTip(value))
            else:
                label.SetLabel(formatAmount(value, prec, lowest, highest))
                label.SetToolTip(wx.ToolTip("%.1f" % value))
        if fit is not None:
            resMax = (lambda: fit.ship.getModifiedItemAttr("cpuOutput"),
                    lambda: fit.ship.getModifiedItemAttr("powerOutput"),
                    lambda: fit.ship.getModifiedItemAttr("droneCapacity"),
                    lambda: fit.ship.getModifiedItemAttr("droneBandwidth"))

        i = 0
        for resourceType in ("cpu", "pg", "droneBay", "droneBandwidth"):
            if fit is not None:
                capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))
                resUsed = getattr(fit,"%sUsed" % resourceType)

                gauge.SetValueRange(resUsed, resMax[i]())

                i+=1
            else:
                capitalizedType = resourceType[0].capitalize() + resourceType[1:]

                gauge = getattr(self, "gauge%s%s" % (panel, capitalizedType))

                gauge.SetValueRange(0, 0)

                i+=1

        self.panel.Layout()
        self.headerPanel.Layout()

ResourcesViewFull.register()
