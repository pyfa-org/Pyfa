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

import wx

class ViewColumn(object):
    '''
    Abstract class that columns can inherit from.
    Once the missing methods are correctly implemented,
    they can be used as columns in a view.
    '''
    columns = {}
    def __init__(self, fittingView):
        self.fittingView = fittingView
        self.columnText = ""
        self.imageId = -1
        self.size = wx.LIST_AUTOSIZE
        self.mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE
        self.resizable = True

    @classmethod
    def register(cls):
        ViewColumn.columns[cls.name] = cls

    @classmethod
    def getColumn(cls, name):
        return ViewColumn.columns[name]

    def getRestrictions(self):
        raise NotImplementedError()

    def getText(self, mod):
        raise NotImplementedError()

    def getImageId(self, mod):
        raise NotImplementedError()

    def getParameters(self):
        raise NotImplementedError()

from gui.builtinViewColumns import *