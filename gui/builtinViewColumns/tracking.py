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
import service
from util import formatAmount
from eos.types import Hardpoint
import wx

class Tracking(ViewColumn):
    name = "Tracking"
    def __init__(self, fittingView, params = None):
        if params == None:
            params = {"showIcon": True,
                      "displayName": False}
        ViewColumn.__init__(self, fittingView)
        cAttribute = service.Attribute.getInstance()
        info = cAttribute.getAttributeInfo("trackingSpeed")
        self.info = info
        if params["showIcon"]:
            iconFile = info.icon.iconFile if info.icon else None
            if iconFile:
                self.imageId = fittingView.imageList.GetImageIndex(iconFile, "pack")
            else:
                self.imageId = -1

            self.mask = wx.LIST_MASK_IMAGE

        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = info.displayName if info.displayName != "" else info.name
            self.mask |= wx.LIST_MASK_TEXT

    def getText(self, stuff):
        trackingSpeed = stuff.getModifiedItemAttr("trackingSpeed")
        if trackingSpeed is not None:
            return (formatAmount(trackingSpeed, 3, 0, 3))
        else:
            if stuff.charge is None:
                return ""

            cloudSize = stuff.getModifiedChargeAttr("aoeCloudSize")
            text = ""
            if cloudSize:
                text += "%s%s" % (formatAmount(cloudSize, 3, 0, 3),
                                  stuff.charge.attributes["aoeCloudSize"].unit.displayName)

            aoeVelocity = stuff.getModifiedChargeAttr("aoeVelocity")
            if aoeVelocity:
                text = "%s | %s%s" % (text,
                                       formatAmount(aoeVelocity, 3, 0, 3),
                                       "m/s") #Hardcoded unit here, m/sec is too long

            return text

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return (("displayName", bool, False),
                ("showIcon", bool, True))
Tracking.register()
