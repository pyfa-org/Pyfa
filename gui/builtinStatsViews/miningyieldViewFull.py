# =============================================================================
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
# =============================================================================

# noinspection PyPackageRequirements
import wx
import gui.mainFrame
from gui.statsView import StatsView
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from service.fit import Fit

_t = wx.GetTranslation

class MiningYieldViewFull(StatsView):
    name = "miningyieldViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []

    def getHeaderText(self, fit):
        return _t("Mining Yield")

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel
        self.headerPanel = headerPanel

        panel = "full"

        sizerMiningYield = wx.FlexGridSizer(1, 4, 0, 0)
        sizerMiningYield.AddGrowableCol(1)

        contentSizer.Add(sizerMiningYield, 0, wx.EXPAND, 0)

        counter = 0

        for miningType, image in (("miner", "mining"), ("drone", "drones")):
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerMiningYield.Add(baseBox, 1, wx.ALIGN_LEFT if counter == 0 else wx.ALIGN_CENTER_HORIZONTAL)

            baseBox.Add(BitmapLoader.getStaticBitmap("%s_big" % image, parent, "gui"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(wx.StaticText(parent, wx.ID_ANY, _t(miningType).capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0 m\u00B3/s")
            setattr(self, "label%sminingyield%s" % (panel.capitalize(), miningType.capitalize()), lbl)

            hbox.Add(lbl, 0, wx.ALIGN_CENTER)
            self._cachedValues.append(0)
            counter += 1
        targetSizer = sizerMiningYield

        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        targetSizer.Add(baseBox, 0, wx.ALIGN_LEFT)

        baseBox.Add(BitmapLoader.getStaticBitmap("cargoBay_big", parent, "gui"), 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        baseBox.Add(box, 0, wx.EXPAND)

        box.Add(wx.StaticText(parent, wx.ID_ANY, _t("Total")), 0, wx.ALIGN_LEFT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 1, wx.EXPAND)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0 m\u00B3/s")
        setattr(self, "label%sminingyieldTotal" % panel.capitalize(), lbl)
        hbox.Add(lbl, 0, wx.ALIGN_LEFT)

        self._cachedValues.append(0)

        image = BitmapLoader.getBitmap("turret_small", "gui")
        firepower = wx.BitmapButton(contentPanel, -1, image)
        firepower.SetToolTip(wx.ToolTip(_t("Click to toggle to Firepower View")))
        firepower.Bind(wx.EVT_BUTTON, self.switchToFirepowerView)
        sizerMiningYield.Add(firepower, 0, wx.ALIGN_LEFT)

        self._cachedValues.append(0)

    def switchToFirepowerView(self, event):
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
        # Get the new view
        view = StatsView.getView("firepowerViewFull")(self.parent)
        view.populatePanel(self.panel, self.headerPanel)
        # Populate us in statsPane's view list
        self.parent.views.append(view)
        # Get the TogglePanel
        tp = self.panel.GetParent()
        # Bind the new panel's children to allow context menu access
        tp.SetLabel(view.getHeaderText(fit))
        view.refreshPanel(fit)

    def refreshPanel(self, fit):
        # If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("labelFullminingyieldMiner", lambda: fit.minerYield, lambda: fit.minerWaste, 3, 0, 0, "{}{} m\u00B3/s", None),
                 ("labelFullminingyieldDrone", lambda: fit.droneYield, lambda: fit.droneWaste, 3, 0, 0, "{}{} m\u00B3/s", None),
                 ("labelFullminingyieldTotal", lambda: fit.totalYield, lambda: fit.totalWaste, 3, 0, 0, "{}{} m\u00B3/s", None))

        def processValue(value):
            value = value() if fit is not None else 0
            value = value if value is not None else 0
            return value

        counter = 0
        for labelName, yieldValue, wasteValue, prec, lowest, highest, valueFormat, altFormat in stats:
            label = getattr(self, labelName)
            yieldValue = processValue(yieldValue)
            wasteValue = processValue(wasteValue)
            if self._cachedValues[counter] != (yieldValue, wasteValue):
                yps = formatAmount(yieldValue, prec, lowest, highest)
                yph = formatAmount(yieldValue * 3600, prec, lowest, highest)
                wps = formatAmount(wasteValue, prec, lowest, highest)
                wph = formatAmount(wasteValue * 3600, prec, lowest, highest)
                wasteSuffix = '\u02b7' if wasteValue > 0 else ''
                label.SetLabel(valueFormat.format(yps, wasteSuffix))
                tipLines = []
                tipLines.append("{} m\u00B3 mining yield per second ({} m\u00B3 per hour)".format(yps, yph))
                if wasteValue > 0:
                    tipLines.append("{} m\u00B3 mining waste per second ({} m\u00B3 per hour)".format(wps, wph))
                label.SetToolTip(wx.ToolTip('\n'.join(tipLines)))
                self._cachedValues[counter] = (yieldValue, wasteValue)
            counter += 1
        self.panel.Layout()
        self.headerPanel.Layout()


MiningYieldViewFull.register()
