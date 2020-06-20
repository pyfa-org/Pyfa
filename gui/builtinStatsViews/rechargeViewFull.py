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

import gui.globalEvents as GE
import gui.mainFrame
from gui.bitmap_loader import BitmapLoader
from gui.statsView import StatsView
from gui.utils.numberFormatter import formatAmount
from service.fit import Fit

_t = wx.GetTranslation


class RechargeViewFull(StatsView):
    name = "rechargeViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.mainFrame.Bind(GE.EFFECTIVE_HP_TOGGLED, self.toggleEffective)

    def getHeaderText(self, fit):
        return _t("Recharge rates")

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    @property
    def effective(self):
        try:
            return self.parent.nameViewMap['resistancesViewFull'].showEffective
        except KeyError:
            return False

    def toggleEffective(self, event):
        event.Skip()
        sFit = Fit.getInstance()
        self.refreshPanel(sFit.getFit(self.mainFrame.getActiveFit()))

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()

        self.panel = contentPanel
        self.headerPanel = headerPanel
        sizerTankStats = wx.FlexGridSizer(3, 5, 0, 0)
        for i in range(4):
            sizerTankStats.AddGrowableCol(i + 1)

        contentSizer.Add(sizerTankStats, 0, wx.EXPAND, 0)

        # Add an empty label first for correct alignment.
        sizerTankStats.Add(wx.StaticText(contentPanel, wx.ID_ANY, ""), 0)
        toolTipText = {
            "shieldPassive": _t("Passive shield recharge"),
            "shieldActive": _t("Active shield boost"),
            "armorActive": _t("Armor repair amount"),
            "hullActive": _t("Hull repair amount")}
        for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
            bitmap = BitmapLoader.getStaticBitmap("%s_big" % tankType, contentPanel, "gui")
            tooltip = wx.ToolTip(toolTipText[tankType])
            bitmap.SetToolTip(tooltip)
            sizerTankStats.Add(bitmap, 0, wx.ALIGN_CENTER)

        toolTipText = {
            "reinforced": _t("Reinforced"),
            "sustained": _t("Sustained")}
        for stability in ("reinforced", "sustained"):
            bitmap = BitmapLoader.getStaticBitmap("regen%s_big" % stability.capitalize(), contentPanel, "gui")
            tooltip = wx.ToolTip(toolTipText[stability])
            bitmap.SetToolTip(tooltip)
            sizerTankStats.Add(bitmap, 0, wx.ALIGN_CENTER)
            for tankType in ("shieldPassive", "shieldActive", "armorActive", "hullActive"):
                if stability == "reinforced" and tankType == "shieldPassive":
                    sizerTankStats.Add(wx.StaticText(contentPanel, wx.ID_ANY, ""))
                    continue

                tankTypeCap = tankType[0].capitalize() + tankType[1:]
                lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.0", style=wx.ALIGN_RIGHT)
                setattr(self, "labelTank%s%s" % (stability.capitalize(), tankTypeCap), lbl)
                box = wx.BoxSizer(wx.HORIZONTAL)
                box.Add(lbl, 0, wx.EXPAND)

                unitlbl = wx.StaticText(contentPanel, wx.ID_ANY, " EHP/s")
                setattr(self, "unitLabelTank%s%s" % (stability.capitalize(), tankTypeCap), unitlbl)
                box.Add(unitlbl, 0, wx.EXPAND)

                sizerTankStats.Add(box, 0, wx.ALIGN_CENTRE)

        contentPanel.Layout()

    def refreshPanel(self, fit):
        # If we did anything interesting, we'd update our labels to reflect the new fit's stats here
        unit = " EHP/s" if self.effective else " HP/s"

        for stability in ("reinforced", "sustained"):
            if stability == "reinforced" and fit is not None:
                tank = fit.effectiveTank if self.effective else fit.tank
            elif stability == "sustained" and fit is not None:
                tank = fit.effectiveSustainableTank if self.effective else fit.sustainableTank
            else:
                tank = None

            for name in ("shield", "armor", "hull"):
                lbl = getattr(self, "labelTank%s%sActive" % (stability.capitalize(), name.capitalize()))
                unitlbl = getattr(self, "unitLabelTank%s%sActive" % (stability.capitalize(), name.capitalize()))
                unitlbl.SetLabel(unit)
                if tank is not None:
                    amount = tank["{}Repair".format(name)]
                else:
                    amount = 0

                if tank is not None and name == "armor":
                    preSpoolAmount = tank["armorRepairPreSpool"]
                    fullSpoolAmount = tank["armorRepairFullSpool"]
                    if round(preSpoolAmount, 1) != round(fullSpoolAmount, 1):
                        ttText = "Spool up: {:.1f}-{:.1f}".format(preSpoolAmount, fullSpoolAmount)
                    else:
                        ttText = ""
                else:
                    ttText = ""

                lbl.SetLabel("{:.1f}{}".format(amount, "\u02e2" if ttText else ""))
                lbl.SetToolTip(wx.ToolTip(ttText))
                unitlbl.SetToolTip(wx.ToolTip(ttText))

        if fit is not None:
            label = getattr(self, "labelTankSustainedShieldPassive")
            value = fit.effectiveTank["passiveShield"] if self.effective else fit.tank["passiveShield"]
            label.SetLabel(formatAmount(value, 3, 0, 9))
            unitlbl = getattr(self, "unitLabelTankSustainedShieldPassive")
            unitlbl.SetLabel(unit)

        else:
            value = 0
            label = getattr(self, "labelTankSustainedShieldPassive")
            label.SetLabel("0")

        label.SetToolTip(wx.ToolTip("%.3f" % value))
        self.panel.Layout()
        self.headerPanel.Layout()


RechargeViewFull.register()
