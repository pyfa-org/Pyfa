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
            gridPrice.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(bitmapLoader.getStaticBitmap(image, contentPanel, "icons"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(contentPanel, wx.ID_ANY, type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00")
            setattr(self, "labelPrice%s" % type.capitalize(), lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

            hbox.Add(wx.StaticText(contentPanel, wx.ID_ANY, " m ISK"), 0, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):
        if fit is not None:
            # Compose a list of all the data we need & request it
            typeIDs = []
            typeIDs.append(fit.ship.item.ID)

            for mod in fit.modules:
                if not mod.isEmpty:
                    typeIDs.append(mod.itemID)

            for drone in fit.drones:
                for _ in xrange(drone.amount):
                    typeIDs.append(drone.itemID)

            cMarket = controller.Market.getInstance()
            cMarket.getPrices(typeIDs, self.processPrices)
        else:
            self.labelPriceShip.SetLabel("0.0")
            self.labelPriceFittings.SetLabel("0.0")
            self.labelPriceTotal.SetLabel("0.0")
            self.panel.Layout()

    def processPrices(self, prices):
        shipPrice = prices[0].price
        modPrice = sum(map(lambda p: p.price, prices[1:]))
        self.labelPriceShip.SetLabel(formatAmount(shipPrice, 3, 3, 9))
        self.labelPriceFittings.SetLabel(formatAmount(modPrice, 3, 3, 9))
        self.labelPriceTotal.SetLabel(formatAmount(shipPrice + modPrice, 3, 3, 9))
        self.panel.Layout()

builtinStatsViews.registerView(PriceViewFull)
