#===============================================================================
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
#===============================================================================

import wx
import service
import gui.mainFrame
from gui.statsView import StatsView
from gui import bitmapLoader
from gui.utils.numberFormatter import formatAmount

class OutgoingViewFull(StatsView):
    name = "outgoingViewFull"
    def __init__(self, parent):
        StatsView.__init__(self)
        self.parent = parent
        self._cachedValues = []
    def getHeaderText(self, fit):
        return "Outgoing"

    def getTextExtentW(self, text):
        width, height = self.parent.GetTextExtent( text )
        return width

    def populatePanel(self, contentPanel, headerPanel):
        contentSizer = contentPanel.GetSizer()
        parent = self.panel = contentPanel
        self.headerPanel = headerPanel

        panel = "full"

        sizerOutgoing = wx.FlexGridSizer(1, 6)
        sizerOutgoing.AddGrowableCol(1)

        contentSizer.Add( sizerOutgoing, 0, wx.EXPAND, 0)

        counter = 0

        for outgoingType, label, image in (("remoteArmor","Armor RR","armorActive") , ("remoteShield","Shield RR","shieldActive")):
            baseBox = wx.BoxSizer(wx.HORIZONTAL)
            sizerOutgoing.Add(baseBox, 1, wx.ALIGN_LEFT if counter == 0 else wx.ALIGN_CENTER_HORIZONTAL)

            baseBox.Add(bitmapLoader.getStaticBitmap("%s_big" % image, parent, "icons"), 0, wx.ALIGN_CENTER)

            box = wx.BoxSizer(wx.VERTICAL)
            baseBox.Add(box, 0, wx.ALIGN_CENTER)

            box.Add(wx.StaticText(parent, wx.ID_ANY, label), 0, wx.ALIGN_LEFT)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            box.Add(hbox, 1, wx.ALIGN_CENTER)

            lbl = wx.StaticText(parent, wx.ID_ANY, u"0.0 HP/s")
            setattr(self, "label%soutgoing%s" % (panel.capitalize() ,outgoingType.capitalize()), lbl)

            hbox.Add(lbl, 0, wx.ALIGN_CENTER)
            self._cachedValues.append(0)
            counter += 1

        targetSizer = sizerOutgoing

        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        targetSizer.Add(baseBox, 0, wx.ALIGN_RIGHT)

        baseBox.Add(bitmapLoader.getStaticBitmap("capacitorInfo_big", parent, "icons"), 0, wx.ALIGN_CENTER)

        gridS = wx.GridSizer(2,2,0,0)

        baseBox.Add(gridS, 0)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0 GJ/s")
        setattr(self, "label%soutgoingRemotecapacitor" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, " +CAP: "), 0, wx.ALL | wx.ALIGN_RIGHT)
        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        self._cachedValues.append(0)

        lbl = wx.StaticText(parent, wx.ID_ANY, "0.0 GJ/s")
        setattr(self, "label%soutgoingNeuting" % panel.capitalize(), lbl)
        gridS.Add(wx.StaticText(parent, wx.ID_ANY, " Neut: "), 0, wx.ALL | wx.ALIGN_RIGHT)

        self._cachedValues.append(0)

        gridS.Add(lbl, 0, wx.ALIGN_LEFT)

        image = bitmapLoader.getBitmap("turret_small", "icons")
        firepower = wx.BitmapButton(contentPanel, -1, image)
        firepower.SetToolTip(wx.ToolTip("Click to toggle to Firepower View"))
        firepower.Bind(wx.EVT_BUTTON, self.switchToFirepowerView)
        sizerOutgoing.Add(firepower, 0, wx.ALIGN_LEFT)

        self._cachedValues.append(0)

    def switchToFirepowerView(self, event):
        # Getting the active fit
        mainFrame = gui.mainFrame.MainFrame.getInstance()
        sFit = service.Fit.getInstance()
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
        tp.SetLabel(view.getHeaderText(fit))
        view.refreshPanel(fit)

    def refreshPanel(self, fit):
        #If we did anything intresting, we'd update our labels to reflect the new fit's stats here

        stats = (("labelFulloutgoingRemotearmor", lambda: fit.armorRR, 3, 0, 0, u"%s HP/s", None),
                 ("labelFulloutgoingRemoteshield", lambda: fit.shieldRR, 3, 0, 0, u"%s HP/s", None),
                 ("labelFulloutgoingRemotecapacitor", lambda: fit.captransfer, 3, 0, 0, u"%s GJ/s",None),
                 ("labelFulloutgoingNeuting", lambda: fit.neut, 3, 0, 0, u"%s GJ/s", None))

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
        
OutgoingViewFull.register()
