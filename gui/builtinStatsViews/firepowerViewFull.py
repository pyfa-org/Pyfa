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
from gui import bitmapLoader
from util import formatAmount

class FirepowerViewFull(StatsView):
    name = "firepowerViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []
    def getHeaderText(self, fit):
        return "Firepower"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel
        self.headerPanel = headerPanel

        panel = "full"

        sizerFirepower = wx.FlexGridSizer(1, 4)
        sizerFirepower.AddGrowableCol(2)

        contentSizer.Add( sizerFirepower, 0, wx.EXPAND, 0)

        counter = 0

        for damageType, image in (("weapon", "turret") , ("drone", "droneDPS")):
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            if counter == 1:
                sizerFirepower.AddSpacer( ( 40, 0), 1, 0, 5 )

            counter += 1
            sizerFirepower.Add(baseBox, 0, wx.ALIGN_LEFT)

            baseBox.Add(bitmapLoader.getStaticBitmap("%s_big" % image, parent, "icons"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(wx.StaticText(parent, wx.ID_ANY, damageType.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0 DPS")
            setattr(self, "label%sDps%s" % (panel.capitalize() ,damageType.capitalize()), lbl)

            hbox.Add(lbl, 0, wx.ALIGN_CENTER)
#            hbox.Add(wx.StaticText(parent, wx.ID_ANY, " DPS"), 0, wx.ALIGN_CENTER)
            self._cachedValues.append(0)
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

        self._cachedValues.append(0)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sDpsTotal" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, " DPS: "), 0, wx.ALL | wx.ALIGN_RIGHT)

        self._cachedValues.append(0)

        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("labelFullDpsWeapon", lambda: fit.weaponDPS, 3, 0, 0, "%s DPS",None),
                 ("labelFullDpsDrone", lambda: fit.droneDPS, 3, 0, 0, "%s DPS", None),
                 ("labelFullVolleyTotal", lambda: fit.weaponVolley, 3, 0, 0, "%s", "Volley: %.1f"),
                 ("labelFullDpsTotal", lambda: fit.totalDPS, 3, 0, 0, "%s", None))

        counter = 0
        for labelName, value, prec, lowest, highest, valueFormat, altFormat in stats:
            label = getattr(self, labelName)
            value = value() if fit is not None else 0
            value = value if value is not None else 0
            if self._cachedValues[counter] != value:
                valueStr = formatAmount(value, prec, lowest, highest)
                label.SetLabel(valueFormat % valueStr)
                tipStr = valueFormat % valueStr if altFormat is None else altFormat % value
                label.SetToolTip(wx.ToolTip(tipStr))
                self._cachedValues[counter] = value
            counter +=1
        self.panel.Layout()
        self.headerPanel.Layout()

FirepowerViewFull.register()
