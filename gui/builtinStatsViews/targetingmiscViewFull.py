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
from util import formatAmount

class TargetingMiscViewFull(StatsView):
    name = "targetingmiscViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
    def getHeaderText(self, fit):
        return "Targeting && Misc"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()

        self.panel = contentPanel
        gridTargetingMisc = wx.FlexGridSizer(1, 3)
        contentSizer.Add( gridTargetingMisc, 0, wx.EXPAND | wx.ALL, 0)
        gridTargetingMisc.AddGrowableCol(0)
        gridTargetingMisc.AddGrowableCol(2)
        # Targeting

        gridTargeting = wx.FlexGridSizer(4, 2)
        gridTargeting.AddGrowableCol(1)

        gridTargetingMisc.Add(gridTargeting, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        labels = (("Targets", "Targets", ""),
                  ("Range", "Range", "km"),
                  ("Scan res.", "ScanRes", "mm"),
                  ("Sensor str.", "SensorStr", ""))

        for header, labelShort, unit in labels:
            gridTargeting.Add(wx.StaticText(contentPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridTargeting.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0")
            setattr(self, "label%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(contentPanel, wx.ID_ANY, " %s" % unit)
            setattr(self, "labelUnit%s" % labelShort, lblUnit)
            box.Add(lblUnit, 0, wx.ALIGN_LEFT)

        # Misc
        gridTargetingMisc.Add( wx.StaticLine( contentPanel, wx.ID_ANY, style = wx.VERTICAL),0, wx.EXPAND, 3 )
        gridMisc = wx.FlexGridSizer(4, 2)
        gridMisc.AddGrowableCol(1)
        gridTargetingMisc.Add(gridMisc,0 , wx.ALIGN_LEFT | wx.ALL, 5)

        labels = (("Speed", "Speed", "m/s"),
                  ("Align time", "AlignTime", "s"),
                  ("Cargo", "Cargo", u"m\u00B3"),
                  ("Signature", "SigRadius", "m"))

        for header, labelShort, unit in labels:
            gridMisc.Add(wx.StaticText(contentPanel, wx.ID_ANY, "%s: " % header), 0, wx.ALIGN_LEFT)

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridMisc.Add(box, 0, wx.ALIGN_LEFT)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0")
            setattr(self, "labelFull%s" % labelShort, lbl)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            lblUnit = wx.StaticText(contentPanel, wx.ID_ANY, " %s" % unit)
            setattr(self, "labelFullUnit%s" % labelShort, lblUnit)
            box.Add(lblUnit, 0, wx.ALIGN_LEFT)



    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("labelTargets", lambda: fit.maxTargets, 3, 0, 0),
                 ("labelRange", lambda: fit.ship.getModifiedItemAttr('maxTargetRange') / 1000, 3, 0, 0),
                 ("labelScanRes", lambda: fit.ship.getModifiedItemAttr('scanResolution'), 3, 0, 0),
                 ("labelSensorStr", lambda: fit.scanStrength, 3, 0, 0),
                 ("labelFullCargo", lambda: fit.extraAttributes["capacity"], 3, 0, 9),
                 ("labelFullSigRadius", lambda: fit.ship.getModifiedItemAttr("signatureRadius"), 3, 0, 9),
                 ("labelFullSpeed", lambda: fit.ship.getModifiedItemAttr("maxVelocity"), 3, 0, 0),
                 ("labelFullAlignTime", lambda: fit.alignTime, 3, 0, 0))

        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName)
            value = value() if fit is not None else 0
            value = value if value is not None else 0
            label.SetLabel(formatAmount(value, prec, lowest, highest))
            if labelName is not "labelSensorStr":
                label.SetToolTip(wx.ToolTip("%.1f" % value))
            else:
                if fit is not None:
                    label.SetToolTip(wx.ToolTip("Type: %s - %.1f" % (fit.scanType, value)))

        self.panel.Layout()

builtinStatsViews.registerView(TargetingMiscViewFull)
