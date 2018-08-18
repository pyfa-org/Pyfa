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


class InsuranceViewFull(StatsView):
    name = "insuranceViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self.insuranceLevels = None

    def getHeaderText(self, fit):
        return "Insurance"

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel
        self.headerPanel = headerPanel
        
        # Column description
        gridInsuranceValues = wx.GridSizer(1, 3, 0, 0)
        contentSizer.Add(gridInsuranceValues, 0, wx.EXPAND | wx.ALL, 0)

        box = wx.BoxSizer(wx.VERTICAL)
        gridInsuranceValues.Add(box, 0, wx.ALIGN_TOP)
        box.Add(wx.StaticText(contentPanel, wx.ID_ANY, "Level"), 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        gridInsuranceValues.Add(box, 0, wx.ALIGN_TOP)
        box.Add(wx.StaticText(contentPanel, wx.ID_ANY, "Cost"), 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        gridInsuranceValues.Add(box, 0, wx.ALIGN_TOP)
        box.Add(wx.StaticText(contentPanel, wx.ID_ANY, "Payout"), 0, wx.ALIGN_CENTER)

        gridInsuranceValues = wx.GridSizer(5, 3, 0, 0)
        contentSizer.Add(gridInsuranceValues, 0, wx.EXPAND | wx.ALL, 0)
        
        for level in ["Basic", "Bronze", "Silver", "Gold", "Platinum"]:
            # Insurance type
            box = wx.BoxSizer(wx.VERTICAL)
            gridInsuranceValues.Add(box, 0, wx.ALIGN_TOP)
            box.Add(wx.StaticText(contentPanel, wx.ID_ANY, level), 0, wx.ALIGN_CENTER)

            # Insurance cost
            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00 ISK")
            setattr(self, "labelInsuranceCost%s" % level, lbl)

            box = wx.BoxSizer(wx.VERTICAL)
            gridInsuranceValues.Add(box, 0, wx.ALIGN_TOP)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

            # Insurance payout
            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00 ISK")
            setattr(self, "labelInsurancePayout%s" % level, lbl)

            box = wx.BoxSizer(wx.VERTICAL)
            gridInsuranceValues.Add(box, 0, wx.ALIGN_TOP)
            box.Add(lbl, 0, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):
        if fit is not None:
            sInsurance = Insurance.getInstance()
            self.insuranceLevels = sInsurance.getInsurance(fit.ship.item.ID)

        self.refreshInsurancePanelPrices()
        self.panel.Layout()

    def refreshInsurancePanelPrices(self):
        if self.insuranceLevels:
            self.labelInsuranceCostBasic.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[0].get('cost'), 3, 3, 9, currency=True))
            self.labelInsurancePayoutBasic.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[0].get('payout'), 3, 3, 9, currency=True))

            self.labelInsuranceCostBronze.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[1].get('cost'), 3, 3, 9, currency=True))
            self.labelInsurancePayoutBronze.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[1].get('payout'), 3, 3, 9, currency=True))

            self.labelInsuranceCostSilver.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[2].get('cost'), 3, 3, 9, currency=True))
            self.labelInsurancePayoutSilver.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[2].get('payout'), 3, 3, 9, currency=True))

            self.labelInsuranceCostGold.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[3].get('cost'), 3, 3, 9, currency=True))
            self.labelInsurancePayoutGold.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[3].get('payout'), 3, 3, 9, currency=True))

            self.labelInsuranceCostPlatinum.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[4].get('cost'), 3, 3, 9, currency=True))
            self.labelInsurancePayoutPlatinum.SetLabel("%s ISK" % formatAmount(self.insuranceLevels[4].get('payout'), 3, 3, 9, currency=True))


InsuranceViewFull.register()
