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
from gui.statsView import StatsView
from gui.bitmapLoader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from service.price import Price


class PriceViewFull(StatsView):
    name = "priceViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedShip = 0
        self._cachedFittings = 0
        self._cachedTotal = 0

    def getHeaderText(self, fit):
        return "Price"

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        self.panel = contentPanel
        self.headerPanel = headerPanel

        headerContentSizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer = headerPanel.GetSizer()
        hsizer.Add(headerContentSizer, 0, 0, 0)
        self.labelEMStatus = wx.StaticText(headerPanel, wx.ID_ANY, "")
        headerContentSizer.Add(self.labelEMStatus)
        headerPanel.GetParent().AddToggleItem(self.labelEMStatus)

        gridPrice = wx.GridSizer(2, 3)
        contentSizer.Add(gridPrice, 0, wx.EXPAND | wx.ALL, 0)
        for type in ("ship", "fittings", "drones", "cargoBay", "character", "total"):
            if type in ("ship"):
                image = "ship_big"
            elif type in ("fittings", "total"):
                image = "%sPrice_big" % type
            else:
                image = "%s_big" % type

            box = wx.BoxSizer(wx.HORIZONTAL)
            gridPrice.Add(box, 0, wx.ALIGN_TOP)

            box.Add(BitmapLoader.getStaticBitmap(image, contentPanel, "gui"), 0, wx.ALIGN_CENTER)

            vbox = wx.BoxSizer(wx.VERTICAL)
            box.Add(vbox, 1, wx.EXPAND)

            vbox.Add(wx.StaticText(contentPanel, wx.ID_ANY, type.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            vbox.Add(hbox)

            lbl = wx.StaticText(contentPanel, wx.ID_ANY, "0.00 ISK")
            setattr(self, "labelPrice%s" % type.capitalize(), lbl)
            hbox.Add(lbl, 0, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):
        if fit is not None:
            self.labelEMStatus.SetLabel("Updating prices...")
            ship_price = Price.fetchItemPrice(fit.ship.item)

            module_price = 0
            if fit.modules:
                for module in fit.modules:
                    if not module.isEmpty:
                        module_price += Price.fetchItemPrice(module.item)

            drone_price = 0
            if fit.drones:
                for drone in fit.drones:
                    drone_price += Price.fetchItemPrice(drone.item) * drone.amount

            fighter_price = 0
            if fit.fighters:
                for fighter in fit.fighters:
                    fighter_price += Price.fetchItemPrice(fighter.item) * fighter.amount

            cargo_price = 0
            if fit.cargo:
                for cargo in fit.cargo:
                    cargo_price += Price.fetchItemPrice(cargo.item) * cargo.amount

            booster_price = 0
            if fit.boosters:
                for booster in fit.boosters:
                    booster_price += Price.fetchItemPrice(booster.item)

            implant_price = 0
            if fit.implants:
                for implant in fit.implants:
                    implant_price += Price.fetchItemPrice(implant.item)

            fitting_price = module_price + drone_price + fighter_price + cargo_price + booster_price + implant_price
            total_price = ship_price + fitting_price

            self.labelPriceShip.SetLabel("%s ISK" % formatAmount(ship_price, 3, 3, 9, currency=True))
            self.labelPriceShip.SetToolTip(wx.ToolTip('{:,.2f}'.format(ship_price)))

            self.labelPriceFittings.SetLabel("%s ISK" % formatAmount(module_price, 3, 3, 9, currency=True))
            self.labelPriceFittings.SetToolTip(wx.ToolTip('{:,.2f}'.format(module_price)))

            self.labelPriceDrones.SetLabel("%s ISK" % formatAmount(drone_price + fighter_price, 3, 3, 9, currency=True))
            self.labelPriceDrones.SetToolTip(wx.ToolTip('{:,.2f}'.format(drone_price + fighter_price)))

            self.labelPriceCargobay.SetLabel("%s ISK" % formatAmount(cargo_price, 3, 3, 9, currency=True))
            self.labelPriceCargobay.SetToolTip(wx.ToolTip('{:,.2f}'.format(cargo_price)))

            self.labelPriceCharacter.SetLabel("%s ISK" % formatAmount(booster_price + implant_price, 3, 3, 9, currency=True))
            self.labelPriceCharacter.SetToolTip(wx.ToolTip('{:,.2f}'.format(booster_price + implant_price)))

            self.labelPriceTotal.SetLabel("%s ISK" % formatAmount(total_price, 3, 3, 9, currency=True))
            self.labelPriceTotal.SetToolTip(wx.ToolTip('{:,.2f}'.format(total_price)))

            self.labelEMStatus.SetLabel("")
            self.panel.Layout()
        else:
            self.labelEMStatus.SetLabel("")
            self.labelPriceShip.SetLabel("0.0 ISK")
            self.labelPriceFittings.SetLabel("0.0 ISK")
            self.labelPriceTotal.SetLabel("0.0 ISK")
            self._cachedFittings = self._cachedShip = self._cachedTotal = 0
            self.panel.Layout()


PriceViewFull.register()
