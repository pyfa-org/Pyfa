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
import controller

class PriceViewFull(StatsView):
    name = "priceViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._timerId = wx.NewId()
        self._timer = None
        self.parent.Bind(wx.EVT_TIMER, self.OnTimer)
        self._timerRunsBeforeUpdate = 60
        self._timerRuns = 0
    def OnTimer( self, event):
        if self._timerId == event.GetId():
            if self._timerRuns >= self._timerRunsBeforeUpdate:
                self._timerRuns = 0
                self._timer.Stop()
                self.refreshPanel(self.fit)
            else:
                self.labelEMStatus.SetLabel("EVE-METRICS prices update retry in: %d seconds" %(self._timerRunsBeforeUpdate - self._timerRuns))
                self._timerRuns += 1
            
    def getHeaderText(self, fit):
        return "Price"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel
        gridPrice = wx.GridSizer(1, 3)
        contentSizer.Add( gridPrice, 0, wx.EXPAND | wx.ALL, 0)
        for type in ("ship", "fittings", "total"):
            image = "%sPrice_big" % type if type != "ship" else "ship_big"
            box = wx.BoxSizer(wx.HORIZONTAL)
            gridPrice.Add(box, 0, wx.ALIGN_TOP)

            box.Add(bitmapLoader.getStaticBitmap(image, contentPanel, "icons"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(contentPanel, wx.ID_ANY, type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00")
            setattr(self, "labelPrice%s" % type.capitalize(), lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

            hbox.Add(wx.StaticText(contentPanel, wx.ID_ANY, " ISK"), 0, wx.ALIGN_LEFT)
        self.labelEMStatus = wx.StaticText(contentPanel, wx.ID_ANY, "")            
        contentSizer.Add(self.labelEMStatus,0)
    def refreshPanel(self, fit):
        if fit is not None:
            self.fit = fit
            # Compose a list of all the data we need & request it
            typeIDs = []
            typeIDs.append(fit.ship.item.ID)

            for mod in fit.modules:
                if not mod.isEmpty:
                    typeIDs.append(mod.itemID)

            for drone in fit.drones:
                for _ in xrange(drone.amount):
                    typeIDs.append(drone.itemID)
            if self._timer:
                if self._timer.IsRunning():
                    self._timer.Stop()
            cMarket = controller.Market.getInstance()
            cMarket.getPrices(typeIDs, self.processPrices)
            self.labelEMStatus.SetLabel("Updating prices from EVE-METRICS...")
        else:
            if self._timer:
                if self._timer.IsRunning():
                    self._timer.Stop()
            self.labelEMStatus.SetLabel("")
            self.labelPriceShip.SetLabel("0.0")
            self.labelPriceFittings.SetLabel("0.0")
            self.labelPriceTotal.SetLabel("0.0")
            self.panel.Layout()

    def processPrices(self, prices):
        shipPrice = prices[0].price
        if shipPrice == None:
            if not self._timer:
                self._timer = wx.Timer(self.parent, self._timerId)
            self._timer.Start(1000)
            self._timerRuns = 0
        else:
            if self._timer:
                self._timer.Stop()
            self.labelEMStatus.SetLabel("")
            modPrice = sum(map(lambda p: p.price or 0, prices[1:]))
            self.labelPriceShip.SetLabel(formatAmount(shipPrice, 3, 3, 9))
            self.labelPriceShip.SetToolTip(wx.ToolTip("%.2f ISK" % shipPrice))
            self.labelPriceFittings.SetLabel(formatAmount(modPrice, 3, 3, 9))
            self.labelPriceFittings.SetToolTip(wx.ToolTip("%.2f ISK" % modPrice))
            self.labelPriceTotal.SetLabel(formatAmount(shipPrice + modPrice, 3, 3, 9))
            self.labelPriceTotal.SetToolTip(wx.ToolTip("%.2f ISK" % (shipPrice + modPrice)))
            self.panel.Layout()

builtinStatsViews.registerView(PriceViewFull)
