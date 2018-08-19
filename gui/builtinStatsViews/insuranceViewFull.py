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

import wx
from gui.statsView import StatsView
from gui.utils.numberFormatter import formatAmount
from service.insurance import Insurance
from service.settings import InsuranceMenuSettings


class InsuranceViewFull(StatsView):
    name = "insuranceViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.insuranceLevels = None
        self.settings = InsuranceMenuSettings.getInstance()
        self.displayColumns = self.getDisplayColumns(self.settings)

    def getDisplayColumns(self, settings):
        return {'cost': self.settings.get("cost"), 'payout': self.settings.get("payout"), 'difference': self.settings.get("difference")}

    ''' Future use when repopulate can be called during runtime, might need rewrite from changing displayColumns from list to dict
    def settingsDiffer(self, settings):
        newColumns = self.getDisplayColumns(settings)
        if self.displayColumns == newColumns:
            return False
        self.displayColumns = newColumns
        return True
    '''

    def getHeaderText(self, fit):
        return "Insurance"

    def newBoxText(self, grid, contentPanel, text):
        box = wx.BoxSizer(wx.VERTICAL)
        grid.Add(box, 0, wx.ALIGN_TOP)
        box.Add(wx.StaticText(contentPanel, wx.ID_ANY, text), 0, wx.ALIGN_CENTER)

    def newBoxLabel(self, grid, contentPanel, labeltype, label):
        lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00 ISK")
        setattr(self, "labelInsurance{}{}".format(labeltype, label), lbl)
        box = wx.BoxSizer(wx.VERTICAL)
        grid.Add(box, 0, wx.ALIGN_TOP)
        box.Add(lbl, 0, wx.ALIGN_LEFT)

    def populatePanel(self, contentPanel, headerPanel, reset=False):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel
        self.headerPanel = headerPanel

        columnCount = sum(self.displayColumns.values()) + 1

        gridInsuranceValues = wx.GridSizer(6, columnCount, 0, 0)
        contentSizer.Add(gridInsuranceValues, 0, wx.EXPAND | wx.ALL, 0)

        self.newBoxText(gridInsuranceValues, contentPanel, "Level")

        if (self.settings.get("cost")):
            self.newBoxText(gridInsuranceValues, contentPanel, "Cost")
        if (self.settings.get("payout")):
            self.newBoxText(gridInsuranceValues, contentPanel, "Payout")
        if (self.settings.get("difference")):
            self.newBoxText(gridInsuranceValues, contentPanel, "Difference")

        for level in ["Basic", "Bronze", "Silver", "Gold", "Platinum"]:
            self.newBoxText(gridInsuranceValues, contentPanel, level)
            if (self.settings.get("cost")):
                self.newBoxLabel(gridInsuranceValues, contentPanel, "Cost", level)
            if (self.settings.get("payout")):
                self.newBoxLabel(gridInsuranceValues, contentPanel, "Payout", level)
            if (self.settings.get("difference")):
                self.newBoxLabel(gridInsuranceValues, contentPanel, "Difference", level)

    def refreshPanel(self, fit):
        if fit is not None:
            sInsurance = Insurance.getInstance()
            self.insuranceLevels = sInsurance.getInsurance(fit.ship.item.ID)

        # Currently populate is only called on init from statsPane.py, so a restart is required for repopulate
        # Could also create the 6 different configurations and enable/disable, but it looks like work is being
        # done to add runtime repopulation of panels, so I'm going to just require restart for column view change
        # to take effect, and then enable this function when the changes for runtime repopulation go live
        # if self.settingsDiffer(self.settings):
            # self.populatePanel(self.panel, self.headerPanel, True)

        self.refreshInsurancePanelPrices()
        self.panel.Layout()

    def refreshInsurancePanelPrices(self):
        if self.insuranceLevels:
            for index, label in enumerate(["Basic", "Bronze", "Silver", "Gold", "Platinum"]):
                cost = self.insuranceLevels[index].get('cost')
                payout = self.insuranceLevels[index].get('payout')
                if self.displayColumns["cost"]:
                    getattr(self, "labelInsuranceCost%s" % label).SetLabel("%s ISK" % formatAmount(cost, 3, 3, 9, currency=True))
                if self.displayColumns["payout"]:
                    getattr(self, "labelInsurancePayout%s" % label).SetLabel("%s ISK" % formatAmount(payout, 3, 3, 9, currency=True))
                if self.displayColumns["difference"]:
                    getattr(self, "labelInsuranceDifference%s" % label).SetLabel("%s ISK" % formatAmount(payout - cost, 3, 3, 9, currency=True))


InsuranceViewFull.register()
