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
from gui.utils.numberFormatter import formatAmount, roundToPrec
from eos.utils.spoolSupport import SpoolType


stats = [
    (
        "labelRemoteCapacitor", "Capacitor:", "{} GJ/s", "capacitorInfo", "Capacitor restored",
        lambda fit: fit.getRemoteReps().get("Capacitor"),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=0).get("Capacitor", 0),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=1).get("Capacitor", 0),
        3, 0, 0),
    (
        "labelRemoteShield", "Shield:", "{} HP/s", "shieldActive", "Shield restored",
        lambda fit: fit.getRemoteReps().get("Shield"),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=0).get("Shield", 0),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=1).get("Shield", 0),
        3, 0, 0),
    (
        "labelRemoteArmor", "Armor:", "{} HP/s", "armorActive", "Armor restored",
        lambda fit: fit.getRemoteReps().get("Armor"),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=0).get("Armor", 0),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=1).get("Armor", 0),
        3, 0, 0),
    (
        "labelRemoteHull", "Hull:", "{} HP/s", "hullActive", "Hull restored",
        lambda fit: fit.getRemoteReps().get("Hull"),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=0).get("Hull", 0),
        lambda fit: fit.getRemoteReps(spoolType=SpoolType.SCALE, spoolAmount=1).get("Hull", 0),
        3, 0, 0)]


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

        sizerOutgoing = wx.GridSizer(1, 4, 0, 0)

        contentSizer.Add(sizerOutgoing, 0, wx.EXPAND, 0)

        for labelName, labelDesc, valueFormat, image, tooltip, val, preSpoolVal, fullSpoolVal, prec, lowest, highest in stats:
            baseBox = wx.BoxSizer(wx.VERTICAL)

            baseBox.Add(wx.StaticText(contentPanel, wx.ID_ANY, labelDesc), 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, valueFormat.format(0))
            lbl.SetToolTip(wx.ToolTip(tooltip))
            setattr(self, labelName, lbl)

            baseBox.Add(lbl, 0, wx.ALIGN_CENTER)
            self._cachedValues.append(0)

            sizerOutgoing.Add(baseBox, 1, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):

        def formatTooltip(text, preSpool, fullSpool, prec, lowest, highest):
            if roundToPrec(preSpool, prec) == roundToPrec(fullSpool, prec):
                return text
            else:
                return "{}, spoolup {}-{}".format(
                    text,
                    formatAmount(preSpool, prec, lowest, highest),
                    formatAmount(fullSpool, prec, lowest, highest))

        counter = 0
        for labelName, labelDesc, valueFormat, image, tooltip, val, preSpoolVal, fullSpoolVal, prec, lowest, highest in stats:
            label = getattr(self, labelName)
            val = val(fit) if fit is not None else 0
            preSpoolVal = preSpoolVal(fit) if fit is not None else 0
            fullSpoolVal = fullSpoolVal(fit) if fit is not None else 0
            # TODO: use spoolup options to fetch main value
            val = fullSpoolVal
            if self._cachedValues[counter] != val:
                label.SetLabel(valueFormat.format(formatAmount(val, prec, lowest, highest)))
                tooltipText = formatTooltip(tooltip, preSpoolVal, fullSpoolVal, prec, lowest, highest)
                label.SetToolTip(wx.ToolTip(tooltipText))
                self._cachedValues[counter] = val
            counter += 1
        self.panel.Layout()
        self.headerPanel.Layout()


OutgoingViewMinimal.register()
