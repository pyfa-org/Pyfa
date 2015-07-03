#===============================================================================
# Copyright (C) 2010 Diego Duclos, Lucas Thode
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

from gui.viewColumn import ViewColumn
from gui import bitmapLoader
from gui.utils.numberFormatter import formatAmount
from eos.types import Drone, Cargo
import wx
import service

class Price(ViewColumn):
    name = "Price"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.mask = wx.LIST_MASK_IMAGE
        self.bitmap = bitmapLoader.getBitmap("totalPrice_small", "icons")
        self.imageId = fittingView.imageList.GetImageIndex("totalPrice_small", "icons")

    def getText(self, stuff):
        if stuff.item is None:
            return ""

        sMkt = service.Market.getInstance()
        price = sMkt.getPriceNow(stuff.item.ID)

        if not price or not price.price or not price.isValid:
            return False

        price = price.price  # Set new price variable with what we need

        if isinstance(stuff, Drone) or isinstance(stuff, Cargo):
           price *= stuff.amount

        return formatAmount(price, 3, 3, 9, currency=True)

    def delayedText(self, mod, display, colItem):
        sMkt = service.Market.getInstance()
        def callback(item):
            price = sMkt.getPriceNow(item.ID)
            text = formatAmount(price.price, 3, 3, 9, currency=True) if price.price else ""
            if price.failed: text += " (!)"
            colItem.SetText(text)

            display.SetItem(colItem)


        sMkt.waitForPrice(mod.item, callback)

    def getImageId(self, mod):
        return -1

    def getToolTip(self, mod):
        return self.name

Price.register()
