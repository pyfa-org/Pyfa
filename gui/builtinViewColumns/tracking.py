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
                self.bitmap = bitmapLoader.getBitmap(iconFile, "pack")
            else:
                self.imageId = -1

            self.mask = wx.LIST_MASK_IMAGE

        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = info.displayName if info.displayName != "" else info.name
            self.mask |= wx.LIST_MASK_TEXT

    def getText(self, stuff):
        item = stuff.item
        if item is None:
            return ""
        itemGroup = item.group.name
        #print(itemGroup)
        if itemGroup in ("Energy Weapon", "Hybrid Weapon", "Projectile Weapon", "Combat Drone", "Fighter Drone"):
            trackingSpeed = stuff.getModifiedItemAttr("trackingSpeed")
            if not trackingSpeed:
                return ""
            return formatAmount(trackingSpeed, 3, 0, 3)
        elif itemGroup in ("Salvager", "Data Miners"):
            chance = stuff.getModifiedItemAttr("accessDifficultyBonus")
            if not chance:
                return ""
            return "{0} %".format(formatAmount(chance, 3, 0, 3))
        elif stuff.charge is not None:
            chargeGroup = stuff.charge.group.name
            print(chargeGroup)
            if chargeGroup in ("Rocket", "Advanced Rocket", "Light Missile", "Advanced Light Missile", "FoF Light Missile",
                               "Assault Missile", "Advanced Assault Missile", "Heavy Missile", "Advanced Heavy Missile", "FoF Heavy Missile",
                               "Torpedo", "Advanced Torpedo", "Cruise Missile", "Advanced Cruise Missile", "FoF Cruise Missile",
                               "Citadel Torpedo", "Citadel Cruise"):
                cloudSize = stuff.getModifiedChargeAttr("aoeCloudSize")
                aoeVelocity = stuff.getModifiedChargeAttr("aoeVelocity")
                if not cloudSize or not aoeVelocity:
                    return ""
                return "{0}{1} | {2}{3}".format(formatAmount(cloudSize, 3, 0, 3), "m",
                                                formatAmount(aoeVelocity, 3, 0, 3), "m/s")
            elif chargeGroup in ("Bomb",):
                cloudSize = stuff.getModifiedChargeAttr("aoeCloudSize")
                if not cloudSize:
                    return ""
                return "{0}{1}".format(formatAmount(cloudSize, 3, 0, 3), "m")
            else:
                return ""
        else:
            return ""

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return (("displayName", bool, False),
                ("showIcon", bool, True))
Tracking.register()
