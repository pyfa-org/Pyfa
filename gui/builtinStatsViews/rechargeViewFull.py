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
from gui import bitmapLoader
from util import formatAmount
import gui.mainFrame
import gui.builtinStatsViews.resistancesViewFull as rvf
import service

class RechargeViewFull(StatsView):
    name = "rechargeViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.mainFrame.Bind(rvf.RAW_HP_ENABLED, self.showRaw)
        self.mainFrame.Bind(rvf.EFFECTIVE_HP_ENABLED, self.showEffective)
        self.effective = True

    def getHeaderText(self, fit):
        return "Recharge rates"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def showRaw(self, event):
        self.effective = False
        sFit = service.Fit.getInstance()
        self.refreshPanel(sFit.getFit(self.mainFrame.getActiveFit()))
        event.Skip()

    def showEffective(self, event):
        self.effective = True
        sFit = service.Fit.getInstance()
        self.refreshPanel(sFit.getFit(self.mainFrame.getActiveFit()))
        event.Skip()

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
        toolTipText = {"shieldPassive" : "Passive shield recharge", "shieldActive" : "Active shield boost", "armorActive" : "Armor repair amount", "hullActive" : "Hull repair amount"}
        for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
            bitmap = bitmapLoader.getStaticBitmap("%s_big" % tankType, contentPanel, "icons")
            tooltip = wx.ToolTip(toolTipText[tankType])
            bitmap.SetToolTip(tooltip)
            sizerTankStats.Add(bitmap, 0, wx.ALIGN_CENTER)

        toolTipText = {"reinforced" : "Reinforced", "sustained" : "Sustained"}
        for stability in ("reinforced", "sustained"):
            bitmap = bitmapLoader.getStaticBitmap("regen%s_big" % stability.capitalize(), contentPanel, "icons")
            tooltip = wx.ToolTip(toolTipText[stability])
            bitmap.SetToolTip(tooltip)
            sizerTankStats.Add(bitmap, 0, wx.ALIGN_CENTER)
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
                tank = fit.effectiveTank if self.effective else fit.tank
            elif stability == "sustained" and fit != None:
                tank = fit.effectiveSustainableTank if self.effective else fit.sustainableTank
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
            value = fit.effectiveTank["passiveShield"] if self.effective else fit.tank["passiveShield"]
            label.SetLabel(formatAmount(value, 3, 0, 9))

        else:
            value = 0
            label = getattr(self, "labelTankSustainedShieldPassive")
            label.SetLabel("0")

        label.SetToolTip(wx.ToolTip("%.3f" % value))
        self.panel.Layout()
        self.headerPanel.Layout()

RechargeViewFull.register()
