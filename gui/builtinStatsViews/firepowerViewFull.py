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
import gui.mainFrame
from gui.statsView import StatsView
from gui.bitmap_loader import BitmapLoader
from gui.utils.numberFormatter import formatAmount
from service.fit import Fit


class FirepowerViewFull(StatsView):
    name = "firepowerViewFull"

    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []

    def getHeaderText(self, fit):
        return "Firepower"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent(text)
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel

        self.headerPanel = headerPanel
        hsizer = self.headerPanel.GetSizer()
        self.stEff = wx.StaticText(self.headerPanel, wx.ID_ANY, "( Effective )")
        hsizer.Add(self.stEff)
        self.headerPanel.GetParent().AddToggleItem(self.stEff)

        panel = "full"

        sizerFirepower = wx.FlexGridSizer(1, 4, 0, 0)
        sizerFirepower.AddGrowableCol(1)

        contentSizer.Add(sizerFirepower, 0, wx.EXPAND, 0)

        counter = 0

        for damageType, image in (("weapon", "turret"), ("drone", "droneDPS")):
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerFirepower.Add(baseBox, 1, wx.ALIGN_LEFT if counter == 0 else wx.ALIGN_CENTER_HORIZONTAL)

            baseBox.Add(BitmapLoader.getStaticBitmap("%s_big" % image, parent, "gui"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(wx.StaticText(parent, wx.ID_ANY, damageType.capitalize()), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, "0.0 DPS")
            setattr(self, "label%sDps%s" % (panel.capitalize(), damageType.capitalize()), lbl)

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
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, " Volley: "), 0, wx.ALL | wx.ALIGN_RIGHT)
        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        self._cachedValues.append(0)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0")
        setattr(self, "label%sDpsTotal" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, " DPS: "), 0, wx.ALL | wx.ALIGN_RIGHT)

        self._cachedValues.append(0)

        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        image = BitmapLoader.getBitmap("mining_small", "gui")
        self.miningyield = wx.BitmapButton(contentPanel, -1, image)
        self.miningyield.SetToolTip(wx.ToolTip("Click to toggle to Mining Yield "))
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
        hsizer = self.headerPanel.GetSizer()
        hsizer.Hide(self.stEff)
        #self.stEff.Destroy()

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
        if fit is not None and fit.targetResists is not None:
            self.stEff.Show()
        else:
            self.stEff.Hide()

        stats = (("labelFullDpsWeapon", lambda: fit.weaponDPS, 3, 0, 0, "%s DPS", None),
                 ("labelFullDpsDrone", lambda: fit.droneDPS, 3, 0, 0, "%s DPS", None),
                 ("labelFullVolleyTotal", lambda: fit.totalVolley, 3, 0, 0, "%s", "Volley: %.1f"),
                 ("labelFullDpsTotal", lambda: fit.totalDPS, 3, 0, 0, "%s", None))
        # See GH issue #
        # if fit is not None and fit.totalYield > 0:
        #    self.miningyield.Show()
        # else:
        #    self.miningyield.Hide()

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


FirepowerViewFull.register()
