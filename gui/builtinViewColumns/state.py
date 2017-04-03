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

from eos.saveddata.fit import Fit
from eos.saveddata.implant import Implant
from eos.saveddata.drone import Drone
from eos.saveddata.module import Module, State as State_, Rack
from gui.viewColumn import ViewColumn

import gui.mainFrame


class State(ViewColumn):
    name = "State"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.resizable = False
        self.size = 16
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_IMAGE

    def getText(self, mod):
        return ""

    def getToolTip(self, mod):
        if isinstance(mod, Module) and not mod.isEmpty:
            return State_.getName(mod.state).title()

    def getImageId(self, stuff):
        generic_active = self.fittingView.imageList.GetImageIndex("state_%s_small" % State_.getName(1).lower(), "gui")
        generic_inactive = self.fittingView.imageList.GetImageIndex("state_%s_small" % State_.getName(-1).lower(),
                                                                    "gui")

        if isinstance(stuff, Drone):
            if stuff.amountActive > 0:
                return generic_active
            else:
                return generic_inactive
        elif isinstance(stuff, Rack):
            return -1
        elif isinstance(stuff, Module):
            if stuff.isEmpty:
                return -1
            else:
                return self.fittingView.imageList.GetImageIndex("state_%s_small" % State_.getName(stuff.state).lower(),
                                                                "gui")
        elif isinstance(stuff, Fit):
            fitID = self.mainFrame.getActiveFit()

            # Can't use isinstance here due to being prevented from importing CommandView.
            # So we do the next best thing and compare Name of class.
            if self.fittingView.__class__.__name__ == "CommandView":
                info = stuff.getCommandInfo(fitID)
            else:
                info = stuff.getProjectionInfo(fitID)

            if info is None:
                return -1
            if info.active:
                return generic_active
            return generic_inactive
        elif isinstance(stuff, Implant) and stuff.character:
            # if we're showing character implants, show an "online" state, which should not be changed
            return self.fittingView.imageList.GetImageIndex("state_%s_small" % State_.getName(0).lower(), "gui")
        else:
            active = getattr(stuff, "active", None)
            if active is None:
                return -1
            if active:
                return generic_active
            return generic_inactive


State.register()
