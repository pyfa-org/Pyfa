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
from gui.statsView import StatsView
from gui import builtinStatsViews

from gui.pyfatogglepanel import TogglePanel
from gui import bitmapLoader
from gui import pygauge as PG

from eos.types import Slot, Hardpoint

from util import formatAmount 

class FirepowerViewFull(StatsView):
    name = "firepowerViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
    def getHeaderText(self, fit):
        return "Firepower"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel):

        contentSizer = contentPanel.GetSizer()


        parent = contentPanel
        panel = "full"
        contentSizer.Add( sizerResources, 0, wx.EXPAND | wx.ALL, 0) 



    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        pass
    
builtinStatsViews.registerView(FirepowerViewFull)
