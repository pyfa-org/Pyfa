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

import gui.mainFrame
from eos.saveddata.drone import Drone
from eos.saveddata.fighter import Fighter
from service.attribute import Attribute
from gui.viewColumn import ViewColumn
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount


_t = wx.GetTranslation


class DroneEhpColumn(ViewColumn):
    name = "Drone HP"

    def __init__(self, fittingView, params=None):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        if params is None:
            params = {"showIcon": True, "displayName": False}

        ViewColumn.__init__(self, fittingView)

        sAttr = Attribute.getInstance()
        info = sAttr.getAttributeInfo("shieldCapacity")
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
        if not isinstance(stuff, (Drone, Fighter)):
            return ""
        if self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective:
            ehp = sum(stuff.ehp.values())
        else:
            ehp = sum(stuff.hp.values())
        return formatAmount(ehp, 3, 0, 9)

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return ("displayName", bool, False), ("showIcon", bool, True)

    def getToolTip(self, stuff):
        if not isinstance(stuff, (Drone, Fighter)):
            return ""
        if self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective:
            return _t("Effective HP")
        else:
            return _t("HP")


DroneEhpColumn.register()
