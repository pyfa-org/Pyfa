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
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount, roundToPrec
from eos.utils.spoolSupport import SpoolType, SpoolOptions
import eos.config

_t = wx.GetTranslation

stats = [
    (
        "labelRemoteCapacitor", "Capacitor:", "{}{} GJ/s", "capacitorInfo", _t("Capacitor restored"),
        lambda fit, spool: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, spool, False)).capacitor,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)).capacitor,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)).capacitor,
        3, 0, 0),
    (
        "labelRemoteShield", "Shield:", "{}{} HP/s", "shieldActive", _t("Shield restored"),
        lambda fit, spool: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, spool, False)).shield,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)).shield,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)).shield,
        3, 0, 0),
    (
        "labelRemoteArmor", "Armor:", "{}{} HP/s", "armorActive", _t("Armor restored"),
        lambda fit, spool: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, spool, False)).armor,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)).armor,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)).armor,
        3, 0, 0),
    (
        "labelRemoteHull", "Hull:", "{}{} HP/s", "hullActive", _t("Hull restored"),
        lambda fit, spool: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, spool, False)).hull,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)).hull,
        lambda fit: fit.getRemoteReps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)).hull,
        3, 0, 0)]


class OutgoingViewFull(StatsView):
    name = "outgoingViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []

    def getHeaderText(self, fit):
        return _t("Remote Reps")

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

            baseBox.Add(BitmapLoader.getStaticBitmap("%s_big" % image, parent, "gui"), 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, valueFormat.format(0, ""))
            lbl.SetToolTip(wx.ToolTip(tooltip))
            setattr(self, labelName, lbl)

            baseBox.Add(lbl, 0, wx.ALIGN_CENTER)
            self._cachedValues.append(0)

            sizerOutgoing.Add(baseBox, 1, wx.ALIGN_LEFT)

    def refreshPanel(self, fit):

        def formatTooltip(text, preSpool, fullSpool, prec, lowest, highest):
            if roundToPrec(preSpool, prec) == roundToPrec(fullSpool, prec):
                return False, text
            else:
                return True, "{}\nSpool up: {}-{}".format(
                    text,
                    formatAmount(preSpool, prec, lowest, highest),
                    formatAmount(fullSpool, prec, lowest, highest))

        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        counter = 0
        for labelName, labelDesc, valueFormat, image, tooltip, val, preSpoolVal, fullSpoolVal, prec, lowest, highest in stats:
            label = getattr(self, labelName)
            val = val(fit, defaultSpoolValue) if fit is not None else 0
            preSpoolVal = preSpoolVal(fit) if fit is not None else 0
            fullSpoolVal = fullSpoolVal(fit) if fit is not None else 0
            if self._cachedValues[counter] != val:
                hasSpool, tooltipText = formatTooltip(tooltip, preSpoolVal, fullSpoolVal, prec, lowest, highest)
                label.SetLabel(valueFormat.format(
                    formatAmount(val, prec, lowest, highest),
                    "\u02e2" if hasSpool else ""))
                label.SetToolTip(wx.ToolTip(tooltipText))
                self._cachedValues[counter] = val
            counter += 1
        self.panel.Layout()
        self.headerPanel.Layout()


OutgoingViewFull.register()
