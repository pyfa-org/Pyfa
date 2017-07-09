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


class ViewColumn(object):
    """
    Abstract class that columns can inherit from.
    Once the missing methods are correctly implemented,
    they can be used as columns in a view.
    """
    columns = {}

    def __init__(self, fittingView):
        self.fittingView = fittingView
        self.columnText = ""
        self.imageId = -1
        self.size = wx.LIST_AUTOSIZE_USEHEADER
        self.mask = 0
        self.maxsize = -1
        self.bitmap = wx.NullBitmap

    @classmethod
    def register(cls):
        ViewColumn.columns[cls.name] = cls

    @classmethod
    def getColumn(cls, name):
        return ViewColumn.columns[name]

    def getRestrictions(self):
        raise NotImplementedError()

    def getText(self, mod):
        return ""

    def getToolTip(self, mod):
        return None

    def getImageId(self, mod):
        return -1

    @staticmethod
    def getParameters():
        return tuple()

    def delayedText(self, display, colItem):
        raise NotImplementedError()


# noinspection PyUnresolvedReferences
from gui.builtinViewColumns import (  # noqa: E402, F401
    abilities,
    ammo,
    ammoIcon,
    attributeDisplay,
    baseIcon,
    baseName,
    capacitorUse,
    maxRange,
    misc,
    price,
    propertyDisplay,
    state,
    sideEffects
)
