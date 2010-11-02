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
import wx

class ModuleAmmoIcon(ViewColumn):
    name = "Module Ammo Icon"
    def __init__(self, fittingView, params):
        ViewColumn.__init__(self, fittingView)
        self.size = 16
        self.mask = wx.LIST_MASK_IMAGE
        self.columnText = ""

    def getText(self, mod):
        return ""

    def getImageId(self, mod):
        if mod.charge is None:
            iconId = -1
        else:
            iconFile = mod.charge.icon.iconFile if mod.item.icon else ""
            if iconFile:
                bitmap = bitmapLoader.getBitmap(iconFile, "pack")
                if bitmap is None:
                    iconId = -1
                else:
                    iconId = self.fittingView.imageList.Add(bitmap)
            else:
                iconId = -1

        return iconId

ModuleAmmoIcon.register()
