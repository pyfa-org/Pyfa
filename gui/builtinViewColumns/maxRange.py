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

from eos.saveddata.mode import Mode
from service.attribute import Attribute
from gui.viewColumn import ViewColumn
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount


class MaxRange(ViewColumn):
    name = "Max Range"

    def __init__(self, fittingView, params=None):
        if params is None:
            params = {"showIcon": True, "displayName": False}

        ViewColumn.__init__(self, fittingView)

        sAttr = Attribute.getInstance()
        info = sAttr.getAttributeInfo("maxRange")
        self.info = info
        if params["showIcon"]:
            iconFile = info.iconID
            if iconFile:
                self.imageId = fittingView.imageList.GetImageIndex(iconFile, "icons")
                self.bitmap = BitmapLoader.getBitmap(iconFile, "icons")
            else:
                self.imageId = -1
            self.mask = wx.LIST_MASK_IMAGE
        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = info.displayName if info.displayName != "" else info.name
            self.mask |= wx.LIST_MASK_TEXT

    def getText(self, stuff):
        if isinstance(stuff, Mode):
            return ""

        maxRange = stuff.maxRange if hasattr(stuff, "maxRange") else stuff.getModifiedItemAttr("maxRange", None)
        falloff = stuff.falloff
        if falloff and falloff >= 5:
            falloff = "+%sm" % formatAmount(falloff, 3, 0, 3)
        else:
            falloff = ""

        if maxRange:
            return "%sm%s" % (formatAmount(maxRange, 3, 0, 3), falloff)
        else:
            return "" + falloff

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return ("displayName", bool, False), ("showIcon", bool, True)

    def getToolTip(self, mod):
        return "Optimal + Falloff"


MaxRange.register()
