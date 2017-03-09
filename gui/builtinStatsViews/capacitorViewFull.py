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
from gui.statsView import StatsView
from gui.bitmapLoader import BitmapLoader
from gui.utils.numberFormatter import formatAmount


class CapacitorViewFull(StatsView):
    name = "capacitorViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent

    def getHeaderText(self, fit):
        return "Capacitor"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel
        self.headerPanel = headerPanel

        panel = "full"

        sizerCapacitor = wx.GridSizer(1, 2)
        contentSizer.Add(sizerCapacitor, 0, wx.EXPAND, 0)
        # Capacitor capacity and time
        baseBox = wx.BoxSizer(wx.HORIZONTAL)

        sizerCapacitor.Add(baseBox, 0, wx.ALIGN_LEFT)
        bitmap = BitmapLoader.getStaticBitmap("capacitorInfo_big", parent, "gui")
        tooltip = wx.ToolTip("Capacitor stability")
        bitmap.SetToolTip(tooltip)
        baseBox.Add(bitmap, 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        baseBox.Add(box, 0, wx.ALIGN_LEFT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 0, wx.ALIGN_LEFT)

        hbox.Add(wx.StaticText(parent, wx.ID_ANY, "Total: "), 0, wx.ALIGN_LEFT | wx.LEFT, 3)
        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sCapacitorCapacity" % panel.capitalize(), lbl)
        hbox.Add(lbl, 0, wx.ALIGN_LEFT)

        hbox.Add(wx.StaticText(parent, wx.ID_ANY, " GJ"), 0, wx.ALIGN_LEFT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 0, wx.ALIGN_LEFT)

        lbl = wx.StaticText(parent, wx.ID_ANY, "Lasts ")
        hbox.Add(lbl, 0, wx.ALIGN_LEFT | wx.LEFT, 3)
        setattr(self, "label%sCapacitorState" % panel.capitalize(), lbl)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0s")
        setattr(self, "label%sCapacitorTime" % panel.capitalize(), lbl)
        hbox.Add(lbl, 0, wx.ALIGN_LEFT)

        # Capacitor balance
        baseBox = wx.BoxSizer(wx.HORIZONTAL)

        sizerCapacitor.Add(baseBox, 0, wx.ALIGN_CENTER_HORIZONTAL)

        tooltip = wx.ToolTip("Capacitor throughput")
        bitmap = BitmapLoader.getStaticBitmap("capacitorRecharge_big", parent, "gui")
        bitmap.SetToolTip(tooltip)
        baseBox.Add(bitmap, 0, wx.ALIGN_CENTER)

        # Recharge
        chargeSizer = wx.FlexGridSizer(2, 3)
        baseBox.Add(chargeSizer, 0, wx.ALIGN_CENTER)

        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, "+ "), 0, wx.ALIGN_CENTER)
        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sCapacitorRecharge" % panel.capitalize(), lbl)
        chargeSizer.Add(lbl, 0, wx.ALIGN_CENTER)
        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

        # Discharge
        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, "- "), 0, wx.ALIGN_CENTER)
        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sCapacitorDischarge" % panel.capitalize(), lbl)
        chargeSizer.Add(lbl, 0, wx.ALIGN_CENTER)
        chargeSizer.Add(wx.StaticText(parent, wx.ID_ANY, " GJ/s"), 0, wx.ALIGN_CENTER)

    def refreshPanel(self, fit):
        # If we did anything intresting, we'd update our labels to reflect the new fit's stats here
        stats = (
            ("label%sCapacitorCapacity", lambda: fit.ship.getModifiedItemAttr("capacitorCapacity"), 3, 0, 9),
            ("label%sCapacitorRecharge", lambda: fit.capRecharge, 3, 0, 0),
            ("label%sCapacitorDischarge", lambda: fit.capUsed, 3, 0, 0),
        )
        if fit:
            neut_resist = fit.ship.getModifiedItemAttr("energyWarfareResistance", 0)
        else:
            neut_resist = 0

        panel = "Full"
        for labelName, value, prec, lowest, highest in stats:
            label = getattr(self, labelName % panel)
            value = value() if fit is not None else 0
            value = value if value is not None else 0
            if isinstance(value, basestring):
                label.SetLabel(value)
                label.SetToolTip(wx.ToolTip(value))
            else:
                label.SetLabel(formatAmount(value, prec, lowest, highest))
                label.SetToolTip(wx.ToolTip("%.1f" % value))

            if labelName == "label%sCapacitorDischarge":
                if neut_resist:
                    neut_resist = 100 - (neut_resist * 100)
                label_tooltip = "Neut Resistance: {0:.0f}%".format(neut_resist)
                label.SetToolTip(wx.ToolTip(label_tooltip))

        capState = fit.capState if fit is not None else 0
        capStable = fit.capStable if fit is not None else False
        lblNameTime = "label%sCapacitorTime"
        lblNameState = "label%sCapacitorState"
        if isinstance(capState, tuple) and len(capState) >= 2:
            t = ("{0}%-{1}%", capState[0], capState[1])
            s = ""
        else:
            if capStable:
                t = "%.1f%%" % capState
            else:
                if capState > 60:
                    t = "%dm%ds" % divmod(capState, 60)
                else:
                    t = "%ds" % capState

            s = "Stable: " if capStable else "Lasts "

        getattr(self, lblNameTime % panel).SetLabel(t)
        getattr(self, lblNameState % panel).SetLabel(s)

        self.panel.Layout()
        self.headerPanel.Layout()


CapacitorViewFull.register()
