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

        sMarket = service.Market.getInstance()
        price = sMarket.getPriceNow(stuff.item.ID)
        return formatAmount(price.price, 3, 3, 9, currency=True) if price and price.price else False

    def delayedText(self, mod, display, colItem):
        def callback(requests):
            price = requests[0].price
            colItem.SetText(formatAmount(price, 3, 3, 9, currency=True) if price else "")
            display.SetItem(colItem)

        service.Market.getInstance().getPrices([mod.item.ID], callback)

    def getImageId(self, mod):
        return -1

Price.register()
