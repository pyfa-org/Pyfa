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
_t = wx.GetTranslation

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
        d.Display.__init__(self, parent, style=wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)

        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDoubleClick)
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
        modifiers = event.GetModifiers()
        if keycode == wx.WXK_ESCAPE and modifiers == wx.MOD_NONE:
            self.unselectAll()
        elif keycode == 65 and modifiers == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and modifiers == wx.MOD_NONE:
            boosters = self.getSelectedBoosters()
            self.removeBoosters(boosters)
        event.Skip()

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if activeFitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            return

        self.original = fit.boosters if fit is not None else None
        self.boosters = fit.boosters[:] if fit is not None else None
        if self.boosters is not None:
            self.boosters.sort(key=lambda booster: booster.slot or 0)

        if activeFitID != self.lastFitId:
            self.lastFitId = activeFitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.update(self.boosters)

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

    def onLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                try:
                    booster = self.boosters[row]
                except IndexError:
                    return
                self.removeBoosters([booster])

    def removeBoosters(self, boosters):
        fitID = self.mainFrame.getActiveFit()
        positions = []
        for booster in boosters:
            if booster in self.original:
                positions.append(self.original.index(booster))
        self.mainFrame.command.Submit(cmd.GuiRemoveBoostersCommand(fitID=fitID, positions=positions))

    def click(self, event):
        mainRow, _ = self.HitTest(event.Position)
        if mainRow != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                try:
                    mainBooster = self.boosters[mainRow]
                except IndexError:
                    return
                if mainBooster in self.original:
                    mainPosition = self.original.index(mainBooster)
                    positions = []
                    for row in self.getSelectedRows():
                        try:
                            booster = self.boosters[row]
                        except IndexError:
                            continue
                        if booster in self.original:
                            positions.append(self.original.index(booster))
                    if mainPosition not in positions:
                        positions = [mainPosition]
                    self.mainFrame.command.Submit(cmd.GuiToggleBoosterStatesCommand(
                        fitID=fitID,
                        mainPosition=mainPosition,
                        positions=positions))
                    return
        event.Skip()

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        selection = self.getSelectedBoosters()
        mainBooster = None
        if clickedPos != -1:
            try:
                booster = self.boosters[clickedPos]
            except IndexError:
                pass
            else:
                if booster in self.original:
                    mainBooster = booster
        itemContext = None if mainBooster is None else _t("Booster")
        menu = ContextMenu.getMenu(self, mainBooster, selection, ("boosterItem", itemContext), ("boosterItemMisc", itemContext))
        if menu:
            self.PopupMenu(menu)

    def getSelectedBoosters(self):
        boosters = []
        for row in self.getSelectedRows():
            try:
                booster = self.boosters[row]
            except IndexError:
                continue
            boosters.append(booster)
        return boosters

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Amount of active boosters
        if opt == 1:
            amount = len([b for b in fit.boosters if b.active])
            return ' ({})'.format(amount) if amount else None
        # Total amount of boosters
        elif opt == 2:
            amount = len(fit.boosters)
            return ' ({})'.format(amount) if amount else None
        else:
            return None
