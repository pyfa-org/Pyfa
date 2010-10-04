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
from util import formatAmount

class RechargeViewFull(StatsView):
    name = "rechargeViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
    def getHeaderText(self, fit):
        return "Recharge rates"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()

        self.panel = contentPanel
        self.headerPanel = headerPanel
        sizerTankStats = wx.FlexGridSizer(3, 5)
        for i in xrange(4):
            sizerTankStats.AddGrowableCol(i + 1)

        contentSizer.Add(sizerTankStats, 0, wx.EXPAND, 0)

        #Add an empty label first for correct alignment.
        sizerTankStats.Add(wx.StaticText(contentPanel, wx.ID_ANY, ""), 0)
        for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
            sizerTankStats.Add(bitmapLoader.getStaticBitmap("%s_big" % tankType, contentPanel, "icons"), 0, wx.ALIGN_CENTER)

        for stability in ("reinforced", "sustained"):
                sizerTankStats.Add(bitmapLoader.getStaticBitmap("regen%s_big" % stability.capitalize(), contentPanel, "icons"), 0, wx.ALIGN_CENTER)
                for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
                    if stability == "reinforced" and tankType == "shieldPassive":
                        sizerTankStats.Add(wx.StaticText(contentPanel, wx.ID_ANY, ""))
                        continue

                    tankTypeCap = tankType[0].capitalize() + tankType[1:]
                    lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.0", style = wx.ALIGN_RIGHT)
                    setattr(self, "labelTank%s%s" % (stability.capitalize(), tankTypeCap), lbl)

                    box = wx.BoxSizer(wx.HORIZONTAL)
                    box.Add(lbl, 0, wx.EXPAND)
                    box.Add(wx.StaticText(contentPanel, wx.ID_ANY, " HP/s"), 0, wx.EXPAND)

                    sizerTankStats.Add(box, 0, wx.ALIGN_CENTRE)

        contentPanel.Layout()

    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        for stability in ("reinforced", "sustained"):
            if stability == "reinforced" and fit != None:
                tank = fit.effectiveTank
            elif stability == "sustained" and fit != None:
                tank = fit.effectiveSustainableTank
            else:
                tank = None


            for name in ("shield", "armor", "hull"):
                lbl = getattr(self, "labelTank%s%sActive" % (stability.capitalize(), name.capitalize()))
                if tank is not None:
                    lbl.SetLabel("%.1f" % tank["%sRepair" % name])
                else:
                    lbl.SetLabel("0.0")
        if fit is not None:
            label = getattr(self, "labelTankSustainedShieldPassive")
            value = fit.calculateShieldRecharge()
            label.SetLabel(formatAmount(value, 3, 0, 9))

        else:
            value = 0
            label = getattr(self, "labelTankSustainedShieldPassive")
            label.SetLabel("0")

        label.SetToolTip(wx.ToolTip("%.3f" % value))
        self.panel.Layout()
        self.headerPanel.Layout()

RechargeViewFull.register()