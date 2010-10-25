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
import service

class ModulePrice(ViewColumn):
    name = "Module Price"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        bitmap = bitmapLoader.getBitmap("totalPrice_small", "icons")
        if bitmap:
            self.imageId = fittingView.imageList.Add(bitmap)
        else:
            self.imageId = -1


    def getText(self, mod):
        itemPrice = None
        def callback(requests):
            itemPrice = requests[0].price
        
        service.Market.getInstance().getPrices([mod.ID], callback)
        if itemPrice is not None:
            return "%.0f" % itemPrice
        else:
            return ""

    def getImageId(self, mod):
        return -1

ModulePrice.register()
