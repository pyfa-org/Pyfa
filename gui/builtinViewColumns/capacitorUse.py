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

from gui.viewColumn import ViewColumn
from gui import bitmapLoader
import service
from util import formatAmount

class CapacitorUse(ViewColumn):
    name = "Capacitor Usage"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        cAttribute = service.Attribute.getInstance()
        info = cAttribute.getAttributeInfo("capacitorNeed")
        bitmap = bitmapLoader.getBitmap(info.icon.iconFile, "pack")
        if bitmap:
            self.imageId = fittingView.imageList.Add(bitmap)
        else:
            self.imageId = -1


    def getText(self, mod):
        capUse = mod.capUse
        if capUse:
            return "%s%s" % ("+" if capUse < 0 else "", (formatAmount(-capUse, 3, 0, 3)))
        else:
            return ""

    def getImageId(self, mod):
        return -1

CapacitorUse.register()
