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

    def populatePanel(self, contentPanel, headerPanel):

        contentSizer = contentPanel.GetSizer()


        parent = contentPanel
        panel = "full"


        sizerFirepower = wx.FlexGridSizer(1, 3)
        for i in xrange(3):
            sizerFirepower.AddGrowableCol(i)


        contentSizer.Add( sizerFirepower, 0, wx.EXPAND, 0)
        
              

        for damageType, image in (("weapon", "turret") , ("drone", "droneBay")):
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerFirepower.Add(baseBox, 0, wx.ALIGN_LEFT)

            baseBox.Add(bitmapLoader.getStaticBitmap("%s_big" % image, parent, "icons"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(wx.StaticText(parent, wx.ID_ANY, damageType.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
            setattr(self, "label%sDps%s" % (panel.capitalize() ,damageType.capitalize()), lbl)

            hbox.Add(lbl, 0, wx.ALIGN_CENTER)
            hbox.Add(wx.StaticText(parent, wx.ID_ANY, " DPS"), 0, wx.ALIGN_CENTER)


        targetSizer = sizerFirepower

        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        targetSizer.Add(baseBox, 0, wx.ALIGN_LEFT)

        baseBox.Add(bitmapLoader.getStaticBitmap("volley_big", parent, "icons"), 0, wx.ALIGN_CENTER)

        gridS = wx.GridSizer(2,2,0,0)

        baseBox.Add(gridS, 0, wx.ALIGN_LEFT)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sVolleyTotal" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, " Volley: "), 0, wx.ALL | wx.ALIGN_RIGHT)
        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sDpsTotal" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, " DPS: "), 0, wx.ALL | wx.ALIGN_RIGHT)
        gridS.Add(lbl, 0, wx.ALIGN_LEFT)



    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("labelFullDpsWeapon", lambda: fit.weaponDPS, 3, 0, 9),
                 ("labelFullDpsDrone", lambda: fit.droneDPS, 3, 0, 9),
                 ("labelFullVolleyTotal", lambda: fit.weaponVolley, 3, 0, 9),
                 ("labelFullDpsTotal", lambda: fit.totalDPS, 3, 0, 9))

        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName)
            value = value() if fit is not None else 0
            value = value if value is not None else 0
            label.SetLabel(formatAmount(value, prec, lowest, highest))
            label.SetToolTip(wx.ToolTip("%.1f" % value))

    
builtinStatsViews.registerView(FirepowerViewFull)
