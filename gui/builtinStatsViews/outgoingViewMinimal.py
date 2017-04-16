# ===============================================================================
# Copyright (C) 2014 Alexandros Kosiaris
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
# ===============================================================================

# noinspection PyPackageRequirements
import wx
from gui.statsView import StatsView
from gui.utils.numberFormatter import formatAmount


class OutgoingViewMinimal(StatsView):
    name = "outgoingViewMinimal"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []

    def getHeaderText(self, fit):
        return "Remote Reps"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel
        self.headerPanel = headerPanel

        sizerOutgoing = wx.GridSizer(1, 4)

        contentSizer.Add(sizerOutgoing, 0, wx.EXPAND, 0)

        counter = 0

        rr_list = [
            ("RemoteCapacitor", "Capacitor:", "capacitorInfo", "Capacitor GJ/s per second transferred remotely."),
            ("RemoteShield", "Shield:", "shieldActive", "Shield hitpoints per second repaired remotely."),
            ("RemoteArmor", "Armor:", "armorActive", "Armor hitpoints per second repaired remotely."),
            ("RemoteHull", "Hull:", "hullActive", "Hull hitpoints per second repaired remotely."),
        ]

        for outgoingType, label, image, tooltip in rr_list:
            baseBox = wx.BoxSizer(wx.VERTICAL)

            baseBox.Add(wx.StaticText(contentPanel, wx.ID_ANY, label), 0, wx.ALIGN_CENTER)

            if "Capacitor" in outgoingType:
                lbl = wx.StaticText(parent, wx.ID_ANY, u"0 GJ/s")
            else:
                lbl = wx.StaticText(parent, wx.ID_ANY, u"0 HP/s")

            lbl.SetToolTip(wx.ToolTip(tooltip))

            setattr(self, "label%s" % outgoingType, lbl)

            baseBox.Add(lbl, 0, wx.ALIGN_CENTER)
            self._cachedValues.append(0)
            counter += 1

            sizerOutgoing.Add(baseBox, 1, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):
        # If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = [
            ("labelRemoteArmor", lambda: fit.remoteReps["Armor"], 3, 0, 0, u"%s HP/s", None),
            ("labelRemoteShield", lambda: fit.remoteReps["Shield"], 3, 0, 0, u"%s HP/s", None),
            ("labelRemoteHull", lambda: fit.remoteReps["Hull"], 3, 0, 0, u"%s HP/s", None),
            ("labelRemoteCapacitor", lambda: fit.remoteReps["Capacitor"], 3, 0, 0, u"%s GJ/s", None),
        ]

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
            counter += 1
        self.panel.Layout()
        self.headerPanel.Layout()


OutgoingViewMinimal.register()
