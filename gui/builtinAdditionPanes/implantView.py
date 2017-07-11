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
import gui.display as d
from gui.builtinMarketBrowser.events import ITEM_SELECTED
import gui.mainFrame
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
import gui.globalEvents as GE
from eos.saveddata.fit import ImplantLocation
from service.fit import Fit
from service.market import Market


class ImplantView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.implantDisplay = ImplantDisplay(self)
        mainSizer.Add(self.implantDisplay, 1, wx.EXPAND, 0)

        radioSizer = wx.BoxSizer(wx.HORIZONTAL)
        radioSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        self.rbFit = wx.RadioButton(self, id=wx.ID_ANY, label="Use Fit-specific Implants", style=wx.RB_GROUP)
        self.rbChar = wx.RadioButton(self, id=wx.ID_ANY, label="Use Character Implants")
        radioSizer.Add(self.rbFit, 0, wx.ALL, 5)
        radioSizer.Add(self.rbChar, 0, wx.ALL, 5)
        radioSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        mainSizer.Add(radioSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, self.rbFit)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioSelect, self.rbChar)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        activeFitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(activeFitID)
        if fit:
            self.source = fit.implantSource
            if fit.implantSource == ImplantLocation.FIT:
                self.rbFit.SetValue(True)
            else:
                self.rbChar.SetValue(True)

        self.rbFit.Enable(fit is not None)
        self.rbChar.Enable(fit is not None)

    def OnRadioSelect(self, event):
        fitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        sFit.toggleImplantSource(fitID, ImplantLocation.FIT if self.rbFit.GetValue() else ImplantLocation.CHARACTER)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


class ImplantDisplay(d.Display):
    DEFAULT_COLS = [
        "State",
        "attr:implantness",
        "Base Icon",
        "Base Name",
        "Price",
    ]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL | wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        if "__WXGTK__" in wx.PlatformInfo:
            self.Bind(wx.EVT_RIGHT_UP, self.scheduleMenu)
        else:
            self.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_NUMPAD_DELETE:
            row = self.GetFirstSelected()
            if row != -1:
                self.removeImplant(self.implants[self.GetItemData(row)])
        event.Skip()

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)

        self.Parent.Parent.Parent.DisablePage(self.Parent, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if event.fitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            event.Skip()
            return

        self.original = fit.implants if fit is not None else None
        self.implants = stuff = fit.appliedImplants if fit is not None else None
        if stuff is not None:
            stuff.sort(key=lambda implant: implant.slot)

        if event.fitID != self.lastFitId:
            self.lastFitId = event.fitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.deselectItems()

        self.update(stuff)
        event.Skip()

    def addItem(self, event):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        fit = sFit.getFit(fitID)

        if not fit or fit.isStructure:
            return

        trigger = sFit.addImplant(fitID, event.itemID)
        if trigger:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
            self.mainFrame.additionsPane.select("Implants")

        event.Skip()

    def removeItem(self, event):
        # Character implants can't be changed here...
        if self.Parent.source == ImplantLocation.CHARACTER:
            return

        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                self.removeImplant(self.implants[self.GetItemData(row)])

    def removeImplant(self, implant):
        fitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()

        sFit.removeImplant(fitID, self.original.index(implant))
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def click(self, event):
        event.Skip()

        # Character implants can't be changed here...
        if self.Parent.source == ImplantLocation.CHARACTER:
            return

        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                sFit = Fit.getInstance()
                sFit.toggleImplant(fitID, row)
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def scheduleMenu(self, event):
        event.Skip()
        if self.getColumn(event.Position) != self.getColIndex(State):
            wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        sel = self.GetFirstSelected()
        menu = None

        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())

        if not fit:
            return

        if sel != -1:
            implant = fit.appliedImplants[sel]

            sMkt = Market.getInstance()
            sourceContext = "implantItem" if fit.implantSource == ImplantLocation.FIT else "implantItemChar"
            itemContext = sMkt.getCategoryByItem(implant.item).name

            menu = ContextMenu.getMenu((implant,), (sourceContext, itemContext))
        elif sel == -1 and fit.implantSource == ImplantLocation.FIT:
            fitID = self.mainFrame.getActiveFit()
            if fitID is None:
                return
            context = (("implantView",),)
            menu = ContextMenu.getMenu([], *context)
        if menu is not None:
            self.PopupMenu(menu)
