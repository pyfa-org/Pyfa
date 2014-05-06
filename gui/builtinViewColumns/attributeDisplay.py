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

from gui import builtinViewColumns
from gui.viewColumn import ViewColumn
from gui import bitmapLoader
from gui.utils.numberFormatter import formatAmount

import service
import wx

class AttributeDisplay(ViewColumn):
    name = "attr"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        cAttribute = service.Attribute.getInstance()
        info = cAttribute.getAttributeInfo(params["attribute"])
        self.info = info
        if params["showIcon"]:
            if info.name == "power":
                iconFile = "pg_small"
                iconType = "icons"
            else:
                iconFile = info.icon.iconFile if info.icon else None
                iconType = "pack"
            if iconFile:
                self.imageId = fittingView.imageList.GetImageIndex(iconFile, iconType)
                self.bitmap = bitmapLoader.getBitmap(iconFile, iconType)
            else:
                self.imageId = -1

            self.mask = wx.LIST_MASK_IMAGE
        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = info.displayName if info.displayName != "" else info.name
            self.mask |= wx.LIST_MASK_IMAGE

        if params["direct"]:
            self.direct = True
            self.view = fittingView
            originalRefresh = fittingView.refresh
            sMarket = service.Market.getInstance()
            #Hack into our master view and add a callback for ourselves to know when to query
            def refresh(stuff):
                self.directInfo = sMarket.directAttrRequest(stuff, info) if stuff else None
                originalRefresh(stuff)

            fittingView.refresh = refresh

    def getText(self, mod):
        if hasattr(mod, "item"):
            attr = mod.getModifiedItemAttr(self.info.name)
        else:
            if self.direct:
                info = self.directInfo
                attr = info.get(mod.ID, "") if info else ""
            else:
                attr = mod.getAttribute(self.info.name)

        if self.info.name == "volume":
            str = (formatAmount(attr, 3, 0, 3))
            if hasattr(mod, "amount"):
                str = str + u"m\u00B3 (%s m\u00B3)"%(formatAmount(attr*mod.amount, 3, 0, 3))
            attr = str

        if isinstance(attr, (float, int)):
            attr = (formatAmount(attr, 3, 0, 3))

        return attr if attr is not None else ""

    def getImageId(self, mod):
        return -1

    @staticmethod
    def getParameters():
        return (("attribute", str, None),
                ("displayName", bool, False),
                ("showIcon", bool, True),
                ("direct", bool, False))

AttributeDisplay.register()
