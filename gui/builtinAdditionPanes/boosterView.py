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
import gui.fitCommands as cmd
import gui.globalEvents as GE
from gui.builtinMarketBrowser.events import ITEM_SELECTED, ItemSelected
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market


class BoosterViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(BoosterViewDrop, self).__init__(*args, **kwargs)
        self.dropFn = dropFn
        # this is really transferring an EVE itemID
        self.dropData = wx.TextDataObject()
        self.SetDataObject(self.dropData)

    def OnData(self, x, y, t):
        if self.GetData():
            dragged_data = DragDropHelper.data
            data = dragged_data.split(':')
            self.dropFn(x, y, data)
        return t


class BoosterView(d.Display):
    DEFAULT_COLS = [
        "State",
        "attr:boosterness",
        "Base Name",
        "Side Effects",
        "Price",
        "Miscellanea",
    ]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL | wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)

        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        self.SetDropTarget(BoosterViewDrop(self.handleListDrag))

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

    def handleListDrag(self, x, y, data):
        """
        Handles dragging of items from various pyfa displays which support it

        data is list with two indices:
            data[0] is hard-coded str of originating source
            data[1] is typeID or index of data we want to manipulate
        """

        if data[0] == "market":
            wx.PostEvent(self.mainFrame, ItemSelected(itemID=int(data[1])))

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        if keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE):
            row = self.GetFirstSelected()
            if row != -1:
                try:
                    booster = self.boosters[self.GetItemData(row)]
                except IndexError:
                    return
                self.removeBooster(booster)

        event.Skip()

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if event.fitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            event.Skip()
            return

        self.original = fit.boosters if fit is not None else None
        self.boosters = fit.boosters[:] if fit is not None else None
        if self.boosters is not None:
            self.boosters.sort(key=lambda booster: booster.slot or 0)

        if event.fitID != self.lastFitId:
            self.lastFitId = event.fitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.update(self.boosters)
        event.Skip()

    def addItem(self, event):
        item = Market.getInstance().getItem(event.itemID, eager='group')
        if item is None or not item.isBooster:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        if not fit or fit.isStructure:
            event.Skip()
            return

        self.mainFrame.command.Submit(cmd.GuiAddBoosterCommand(fitID=fitID, itemID=event.itemID))
        # Select in any case - as we might've added booster which has been there already and command failed
        self.mainFrame.additionsPane.select('Boosters')
        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                try:
                    booster = self.boosters[self.GetItemData(row)]
                except IndexError:
                    return
                self.removeBooster(booster)

    def removeBooster(self, booster):
        fitID = self.mainFrame.getActiveFit()
        if booster in self.original:
            position = self.original.index(booster)
            self.mainFrame.command.Submit(cmd.GuiRemoveBoosterCommand(
                fitID=fitID, position=position))

    def click(self, event):
        event.Skip()
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                try:
                    booster = self.boosters[self.GetItemData(row)]
                except IndexError:
                    return
                if booster in self.original:
                    position = self.original.index(booster)
                    self.mainFrame.command.Submit(cmd.GuiToggleBoosterStateCommand(
                        fitID=fitID,
                        position=position))

    def spawnMenu(self, event):
        sel = self.GetFirstSelected()
        if sel != -1:
            try:
                booster = self.boosters[sel]
            except IndexError:
                return None
            srcContext = "boosterItem"
            itemContext = "Booster"
            menu = ContextMenu.getMenu(booster, (booster,), (srcContext, itemContext))
            self.PopupMenu(menu)
