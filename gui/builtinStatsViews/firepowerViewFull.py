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

import eos.config
import gui.mainFrame
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from gui.bitmap_loader import BitmapLoader
from gui.statsView import StatsView
from gui.utils.numberFormatter import formatAmount, roundToPrec
from service.fit import Fit

_t = wx.GetTranslation


class FirepowerViewFull(StatsView):
    name = "firepowerViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []

    def getHeaderText(self, fit):
        return _t("Firepower")

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel

        self.headerPanel = headerPanel
        hsizer = self.headerPanel.Parent.GetHeaderContentSizer()
        self.stEff = wx.StaticText(self.headerPanel, wx.ID_ANY, "( Effective )")
        hsizer.Insert(0, self.stEff)

        panel = "full"

        sizerFirepower = wx.FlexGridSizer(1, 4, 0, 0)
        sizerFirepower.AddGrowableCol(1)

        contentSizer.Add(sizerFirepower, 0, wx.EXPAND, 0)

        counter = 0

        for label, image, attr in ((_t("Weapon"), "turret", "Weapon"), (_t("Drone"), "droneDPS", "Drone")):
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerFirepower.Add(baseBox, 1, wx.ALIGN_LEFT if counter == 0 else wx.ALIGN_CENTER_HORIZONTAL)

            baseBox.Add(BitmapLoader.getStaticBitmap("%s_big" % image, parent, "gui"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(wx.StaticText(parent, wx.ID_ANY, label), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0 DPS")
            setattr(self, "label%sDps%s" % (panel.capitalize(), attr), lbl)

            hbox.Add(lbl, 0, wx.ALIGN_CENTER)
            self._cachedValues.append(0)
            counter += 1
        targetSizer = sizerFirepower

        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        targetSizer.Add(baseBox, 0, wx.ALIGN_RIGHT)

        baseBox.Add(BitmapLoader.getStaticBitmap("volley_big", parent, "gui"), 0, wx.ALIGN_CENTER)

        gridS = wx.GridSizer(2, 2, 0, 0)

        baseBox.Add(gridS, 0)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sVolleyTotal" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, _t(" Volley: ")), 0, wx.ALL | wx.ALIGN_RIGHT)
        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        self._cachedValues.append(0)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sDpsTotal" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, _t(" DPS: ")), 0, wx.ALL | wx.ALIGN_RIGHT)

        self._cachedValues.append(0)

        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        image = BitmapLoader.getBitmap("mining_small", "gui")
        self.miningyield = wx.BitmapButton(contentPanel, -1, image)
        self.miningyield.SetToolTip(wx.ToolTip(_t("Click to toggle to Mining Yield")))
        self.miningyield.Bind(wx.EVT_BUTTON, self.switchToMiningYieldView)
        sizerFirepower.Add(self.miningyield, 0, wx.ALIGN_LEFT)

        self._cachedValues.append(0)

    def switchToMiningYieldView(self, event):
        # Getting the active fit
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        sFit = Fit.getInstance()
        fit = sFit.getFit(mainFrame.getActiveFit())
        # Remove ourselves from statsPane's view list
        self.parent.views.remove(self)
        self._cachedValues = []
        # And no longer display us
        self.panel.GetSizer().Clear(True)
        self.panel.GetSizer().Layout()

        # Remove effective label
        hsizer = self.headerPanel.Parent.GetHeaderContentSizer()
        for i, c in enumerate(hsizer.Children):
            if c.GetWindow() is self.stEff:
                hsizer.Remove(i)
                self.stEff.Destroy()
                break

        # Get the new view
        view = StatsView.getView("miningyieldViewFull")(self.parent)
        view.populatePanel(self.panel, self.headerPanel)
        # Populate us in statsPane's view list
        self.parent.views.append(view)
        # Get the TogglePanel
        tp = self.panel.GetParent()
        tp.SetLabel(view.getHeaderText(fit))
        view.refreshPanel(fit)

    def refreshPanel(self, fit):
        # If we did anything intresting, we'd update our labels to reflect the new fit's stats here
        if fit is not None and fit.targetProfile is not None:
            self.stEff.Show()
        else:
            self.stEff.Hide()

        def hasSpoolUp(preSpool, fullSpool):
            if preSpool is None or fullSpool is None:
                return False
            return roundToPrec(preSpool.total, prec) != roundToPrec(fullSpool.total, prec)

        def dpsToolTip(normal, preSpool, fullSpool, prec, lowest, highest):
            if normal is None or preSpool is None or fullSpool is None:
                return ""
            hasSpool = hasSpoolUp(preSpool, fullSpool)
            lines = []
            if hasSpool:
                lines.append(_t("Spool up") + ": {}-{}".format(
                        formatAmount(preSpool.total, prec, lowest, highest),
                        formatAmount(fullSpool.total, prec, lowest, highest)))
            if getattr(normal, 'total', None):
                if hasSpool:
                    lines.append("")
                    lines.append(_t("Current") + ": {}".format(formatAmount(normal.total, prec, lowest, highest)))
                for dmgType in normal.names():
                    val = getattr(normal, dmgType, None)
                    if val:
                        lines.append("{}{}: {}%".format(
                                "  " if hasSpool else "",
                                _t(dmgType).capitalize(),
                                formatAmount(val / normal.total * 100, 3, 0, 0)))
            return "\n".join(lines)

        defaultSpoolValue = eos.config.settings['globalDefaultSpoolupPercentage']
        stats = (
            (
                "labelFullDpsWeapon",
                lambda: fit.getWeaponDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)),
                lambda: fit.getWeaponDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)),
                lambda: fit.getWeaponDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)),
                3, 0, 0, "{}{} DPS"),
            (
                "labelFullDpsDrone",
                lambda: fit.getDroneDps(),
                lambda: fit.getDroneDps(),
                lambda: fit.getDroneDps(),
                3, 0, 0, "{}{} DPS"),
            (
                "labelFullVolleyTotal",
                lambda: fit.getTotalVolley(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)),
                lambda: fit.getTotalVolley(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)),
                lambda: fit.getTotalVolley(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)),
                3, 0, 0, "{}{}"),
            (
                "labelFullDpsTotal",
                lambda: fit.getTotalDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpoolValue, False)),
                lambda: fit.getTotalDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True)),
                lambda: fit.getTotalDps(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True)),
                3, 0, 0, "{}{}"))

        counter = 0
        for labelName, val, preSpoolVal, fullSpoolVal, prec, lowest, highest, valueFormat in stats:
            label = getattr(self, labelName)
            val = val() if fit is not None else None
            preSpoolVal = preSpoolVal() if fit is not None else None
            fullSpoolVal = fullSpoolVal() if fit is not None else None
            if self._cachedValues[counter] != val:
                tooltipText = dpsToolTip(val, preSpoolVal, fullSpoolVal, prec, lowest, highest)
                label.SetLabel(valueFormat.format(
                        formatAmount(0 if val is None else val.total, prec, lowest, highest),
                        "\u02e2" if hasSpoolUp(preSpoolVal, fullSpoolVal) else ""))
                label.SetToolTip(wx.ToolTip(tooltipText))
                self._cachedValues[counter] = val
            counter += 1

        self.panel.Layout()
        self.headerPanel.Layout()


FirepowerViewFull.register()
