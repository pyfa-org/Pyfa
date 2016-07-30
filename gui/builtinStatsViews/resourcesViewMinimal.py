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
from gui.bitmapLoader import BitmapLoader
from gui import pygauge as PG
import gui.mainFrame
import gui.chromeTabs

from eos.types import Hardpoint

from gui.utils.numberFormatter import formatAmount

class ResourcesViewMinimal(StatsView):
    name = "resourcesViewMinimal"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def getHeaderText(self, fit):
        return "Fitting Resources"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):

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
        sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        #Turrets & launcher hardslots display
        tooltipText = {"cpu":"CPU", "pg":"PowerGrid", "turret":"Turret hardpoints", "launcher":"Launcher hardpoints", "drones":"Drones active", "fighter": "Fighter squadrons active", "calibration":"Calibration"}
        for type in ("cpu", "pg", "calibration"):
            box = wx.BoxSizer(wx.HORIZONTAL)

            bitmap = BitmapLoader.getStaticBitmap("%s_big" % type, parent, "gui")
            tooltip = wx.ToolTip(tooltipText[type])
            bitmap.SetToolTip(tooltip)

            box.Add(bitmap, 0, wx.ALIGN_CENTER)

            sizer.Add(box, 0, wx.ALIGN_CENTER)

            suffix = {"cpu":"tf", "pg":"MW", 'turret':'Hardpoints', 'launcher':'Hardpoints', 'drones':'Active', 'fighter':'Tubes', 'calibration':'Points'}
            lbl = wx.StaticText(parent, wx.ID_ANY, "0")
            attr = "label%sUsed%s%s" % (panel.capitalize(), type.capitalize(), suffix[type].capitalize())
            setattr(self, attr, lbl)
            box.Add(lbl, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            box.Add(wx.StaticText(parent, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0")
            attr = "label%sTotal%s%s" % (panel.capitalize(), type.capitalize(), suffix[type].capitalize())
            setattr(self, attr, lbl)
            box.Add(lbl, 0, wx.ALIGN_CENTER)
            setattr(self, "boxSizer{}".format(type.capitalize()), box)

            # Hack - We add a spacer after each thing, but we are always hiding something. The spacer is stil there.
            # This way, we only have one space after the drones/fighters
            if type != "drones":
                sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)


    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("label%sUsedCalibrationPoints", lambda: fit.calibrationUsed, 0, 0, 0),
                    ("label%sTotalCalibrationPoints", lambda: fit.ship.getModifiedItemAttr('upgradeCapacity'), 0, 0, 0),
                    ("label%sUsedPgMw", lambda: fit.pgUsed, 0, 0, 0),
                    ("label%sUsedCpuTf", lambda: fit.cpuUsed, 0, 0, 0),
                    ("label%sTotalPgMw", lambda: fit.ship.getModifiedItemAttr("powerOutput"), 0, 0, 0),
                    ("label%sTotalCpuTf", lambda: fit.ship.getModifiedItemAttr("cpuOutput"), 0, 0, 0),
                 )
        panel = "Full"

        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName % panel)
            value = value() if fit is not None else 0
            value = value if value is not None else 0

            if labelName % panel == "label%sUsedCpuTf" % panel:
                usedCpuTf = value
                labelUCPU = label

            if labelName % panel == "label%sTotalCpuTf" % panel:
                totalCpuTf = value
                labelTCPU = label

            if labelName % panel == "label%sUsedPgMw" % panel:
                usedPgMw = value
                labelUPG = label

            if labelName % panel == "label%sTotalPgMw" % panel:
                totalPgMw = value
                labelTPG = label

            if labelName % panel == "label%sUsedCalibrationPoints" % panel:
                usedCalibrationPoints = value
                labelUCP = label

            if labelName % panel == "label%sTotalCalibrationPoints" % panel:
                totalCalibrationPoints = value
                labelTCP = label

            if isinstance(value, basestring):
                label.SetLabel(value)
                label.SetToolTip(wx.ToolTip(value))
            else:
                label.SetLabel(formatAmount(value, prec, lowest, highest))
                label.SetToolTip(wx.ToolTip("%.1f" % value))

        colorWarn = wx.Colour(204, 51, 51)
        colorNormal = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)

        if usedCpuTf > totalCpuTf:
            colorCPU = colorWarn
        else:
            colorCPU = colorNormal

        if usedPgMw > totalPgMw:
            colorPG = colorWarn
        else:
            colorPG = colorNormal

        if usedCalibrationPoints > totalCalibrationPoints:
            colorC = colorWarn
        else:
            colorC = colorNormal

        labelUCPU.SetForegroundColour(colorCPU)
        labelTCPU.SetForegroundColour(colorCPU)
        labelUPG.SetForegroundColour(colorPG)
        labelTPG.SetForegroundColour(colorPG)
        labelUCP.SetForegroundColour(colorC)
        labelTCP.SetForegroundColour(colorC)

        if fit is not None:
            resMax = (lambda: fit.ship.getModifiedItemAttr("cpuOutput"),
                        lambda: fit.ship.getModifiedItemAttr("powerOutput"),
                    )


        self.panel.Layout()
        self.headerPanel.Layout()

ResourcesViewMinimal.register()
