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

from eos.saveddata.module import Module, Rack
from gui.utils.numberFormatter import formatAmount
from gui.viewColumn import ViewColumn


class Pulse(ViewColumn):
    name = "Pulse"

    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.columnText = "Pulse"
        self.resizable = False
        self.size = 58
        self.maxsize = self.size
        self.mask = wx.LIST_MASK_TEXT

    def getText(self, mod):
        if isinstance(mod, Rack):
            return ""
        if isinstance(mod, Module) and not mod.isEmpty:
            if mod.pulseInterval is None:
                return ""
            return formatAmount(mod.pulseInterval, prec=3, unitName="s")
        return ""

    def getToolTip(self, mod):
        if isinstance(mod, Module) and not mod.isEmpty:
            if mod.pulseInterval is None:
                return "Pulse disabled"
            return "Pulse every {} seconds".format(formatAmount(mod.pulseInterval, prec=3))
        return None

    def getImageId(self, mod):
        return -1


Pulse.register()
