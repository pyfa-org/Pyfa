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
from gui.viewColumn import ViewColumn
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount


_t = wx.GetTranslation


class DroneRegenColumn(ViewColumn):
    name = "Drone Regen"

    def __init__(self, fittingView, params=None):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        if params is None:
            params = {"showIcon": True, "displayName": False}

        ViewColumn.__init__(self, fittingView)

        if params["showIcon"]:
            self.imageId = fittingView.imageList.GetImageIndex("shieldPassive_small", "gui")
            self.bitmap = BitmapLoader.getBitmap("shieldPassive_small", "gui")
            self.mask = wx.LIST_MASK_IMAGE
        else:
            self.imageId = -1

        if params["displayName"] or self.imageId == -1:
            self.columnText = _("Misc data")
            self.mask |= wx.LIST_MASK_TEXT

    def getText(self, stuff):
        if not isinstance(stuff, (Drone, Fighter)):
            return ""
        regen = stuff.calculateShieldRecharge()
        if (
            self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective
            and stuff.owner and stuff.owner.damagePattern is not None
        ):
            regen = stuff.owner.damagePattern.effectivify(stuff, regen, 'shield')
        return '{}/s'.format(formatAmount(regen, 3, 0, 9))

    def getImageId(self, mod):
        return -1

    def getParameters(self):
        return ("displayName", bool, False), ("showIcon", bool, True)

    def getToolTip(self, stuff):
        if not isinstance(stuff, (Drone, Fighter)):
            return ""
        if self.mainFrame.statsPane.nameViewMap["resistancesViewFull"].showEffective:
            return _t("Effective Shield Regeneration")
        else:
            return _t("Shield Regeneration")


DroneRegenColumn.register()
