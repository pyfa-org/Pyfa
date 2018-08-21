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

from gui.viewColumn import ViewColumn
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount

from service.attribute import Attribute
from service.market import Market


class AttributeDisplay(ViewColumn):
    name = "attr"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        sAttr = Attribute.getInstance()
        info = sAttr.getAttributeInfo(params["attribute"])
        self.info = info
        if params["showIcon"]:
            if info.name == "power":
                iconFile = "pg_small"
                iconType = "gui"
            else:
                iconFile = info.iconID
                iconType = "icons"
            if iconFile:
                self.imageId = fittingView.imageList.GetImageIndex(iconFile, iconType)
                self.bitmap = BitmapLoader.getBitmap(iconFile, iconType)
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
            sMkt = Market.getInstance()

            def refresh(stuff):
                # Hack into our master view and add a callback for ourselves to know when to query
                self.directInfo = sMkt.directAttrRequest(stuff, info) if stuff else None
                originalRefresh(stuff)

            fittingView.refresh = refresh

    def getText(self, mod):
        if hasattr(mod, "item"):
            attr = mod.getModifiedItemAttr(self.info.name, None)
        else:
            if self.direct:
                info = self.directInfo
                attr = info.get(mod.ID, "") if info else ""
            else:
                attr = mod.getAttribute(self.info.name)

        if attr is None:
            return ""

        if self.info.name == "volume":
            str_ = (formatAmount(attr, 3, 0, 3))
            if hasattr(mod, "amount"):
                str_ += "m\u00B3 (%s m\u00B3)" % (formatAmount(attr * mod.amount, 3, 0, 3))
            attr = str_

        if isinstance(attr, (float, int)):
            attr = (formatAmount(attr, 3, 0, 3))

        return attr

    def getImageId(self, mod):
        return -1

    def getToolTip(self, stuff):
        if self.info.name == "cpu":
            return "CPU"
        else:
            return self.info.name.title()

    @staticmethod
    def getParameters():
        return (("attribute", str, None),
                ("displayName", bool, False),
                ("showIcon", bool, True),
                ("direct", bool, False))


AttributeDisplay.register()
