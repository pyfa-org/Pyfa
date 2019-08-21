# =============================================================================
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
# =============================================================================

# noinspection PyPackageRequirements
import wx

from eos.saveddata.cargo import Cargo
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from eos.saveddata.module import Module
from eos.saveddata.price import PriceStatus
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn
from service.price import Price as ServicePrice


def formatPrice(stuff, priceObj):
    textItems = []
    if priceObj.price:
        mult = 1
        if isinstance(stuff, (Drone, Fighter, Cargo)):
            mult = stuff.amount
        textItems.append(formatAmount(priceObj.price * mult, 3, 3, 9, currency=True))
    if priceObj.status in (PriceStatus.fetchFail, PriceStatus.fetchTimeout):
        textItems.append("(!)")
    return " ".join(textItems)


class Price(ViewColumn):
    name = "Price"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.mask = wx.LIST_MASK_IMAGE
        self.bitmap = BitmapLoader.getBitmap("totalPrice_small", "gui")
        self.imageId = fittingView.imageList.GetImageIndex("totalPrice_small", "gui")

    def getText(self, stuff):
        if stuff.item is None or stuff.item.group.name == "Ship Modifiers":
            return ""

        if hasattr(stuff, "isEmpty"):
            if stuff.isEmpty:
                return ""

        if isinstance(stuff, Module) and stuff.isMutated:
            return ""

        priceObj = stuff.item.price

        if not priceObj.isValid():
            return False

        return formatPrice(stuff, priceObj)

    def delayedText(self, mod, display, colItem):
        sPrice = ServicePrice.getInstance()

        def callback(item):
            priceObj = item[0]
            colItem.SetText(formatPrice(mod, priceObj))

            display.SetItem(colItem)

        sPrice.getPrices([mod.item], callback, waitforthread=True)

    def getImageId(self, mod):
        return -1

    def getToolTip(self, mod):
        return self.name


Price.register()
