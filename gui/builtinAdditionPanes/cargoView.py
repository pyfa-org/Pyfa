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
from gui.contextMenu import ContextMenu
from gui.builtinMarketBrowser.events import ITEM_SELECTED, ItemSelected
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market


class CargoViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(CargoViewDrop, self).__init__(*args, **kwargs)
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


# @todo: Was copied form another class and modified. Look through entire file, refine
class CargoView(d.Display):
    DEFAULT_COLS = ["Base Icon",
                    "Base Name",
                    "attr:volume",
                    "Price"]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDoubleClick)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        self.SetDropTarget(CargoViewDrop(self.handleListDrag))
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

    def addItem(self, event):
        item = Market.getInstance().getItem(event.itemID, eager='group')
        if item is None or not (item.isCharge or item.isCommodity):
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        if not fit:
            event.Skip()
            return
        modifiers = wx.GetMouseState().GetModifiers()
        amount = 1
        if modifiers == wx.MOD_CONTROL:
            amount = 10
        elif modifiers == wx.MOD_ALT:
            amount = 100
        elif modifiers == wx.MOD_CONTROL | wx.MOD_ALT:
            amount = 1000
        self.mainFrame.command.Submit(cmd.GuiAddCargoCommand(
            fitID=fitID, itemID=item.ID, amount=amount))
        self.mainFrame.additionsPane.select('Cargo')
        event.Skip()

    def handleListDrag(self, x, y, data):
        """
        Handles dragging of items from various pyfa displays which support it

        data is list with two indices:
            data[0] is hard-coded str of originating source
            data[1] is typeID or index of data we want to manipulate
        """

        if data[0] == "fitting":
            self.swapModule(x, y, int(data[1]))
        elif data[0] == "market":
            fitID = self.mainFrame.getActiveFit()
            if fitID:
                self.mainFrame.command.Submit(cmd.GuiAddCargoCommand(
                    fitID=fitID, itemID=int(data[1]), amount=1))

    def startDrag(self, event):
        row = event.GetIndex()

        if row != -1:
            data = wx.TextDataObject()
            try:
                dataStr = "cargo:{}".format(self.cargo[row].itemID)
            except IndexError:
                return
            data.SetText(dataStr)

            self.unselectAll()
            self.Select(row, True)

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            DragDropHelper.data = dataStr
            dropSource.DoDragDrop()

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()
        if keycode == wx.WXK_ESCAPE and modifiers == wx.MOD_NONE:
            self.unselectAll()
        elif keycode == 65 and modifiers == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and modifiers == wx.MOD_NONE:
            cargos = self.getSelectedCargos()
            self.removeCargos(cargos)
        event.Skip()

    def swapModule(self, x, y, modIdx):
        """Swap a module from fitting window with cargo"""
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())
        dstRow, _ = self.HitTest((x, y))

        if dstRow > -1:
            try:
                dstCargoItemID = getattr(self.cargo[dstRow], 'itemID', None)
            except IndexError:
                dstCargoItemID = None
        else:
            dstCargoItemID = None

        self.mainFrame.command.Submit(cmd.GuiLocalModuleToCargoCommand(
            fitID=self.mainFrame.getActiveFit(),
            modPosition=modIdx,
            cargoItemID=dstCargoItemID,
            copy=wx.GetMouseState().GetModifiers() == wx.MOD_CONTROL))

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)

        # self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if activeFitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            return

        self.original = fit.cargo if fit is not None else None
        self.cargo = fit.cargo[:] if fit is not None else None
        if self.cargo is not None:
            self.cargo.sort(key=lambda c: (c.item.group.category.name, c.item.group.name, c.item.name))

        if activeFitID != self.lastFitId:
            self.lastFitId = activeFitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.populate(self.cargo)
        self.refresh(self.cargo)

    def onLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            try:
                cargo = self.cargo[row]
            except IndexError:
                return
            self.removeCargos([cargo])

    def removeCargos(self, cargos):
        fitID = self.mainFrame.getActiveFit()
        itemIDs = []
        for cargo in cargos:
            if cargo in self.original:
                itemIDs.append(cargo.itemID)
        self.mainFrame.command.Submit(cmd.GuiRemoveCargosCommand(fitID=fitID, itemIDs=itemIDs))

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        selection = self.getSelectedCargos()
        mainCargo = None
        if clickedPos != -1:
            try:
                cargo = self.cargo[clickedPos]
            except IndexError:
                pass
            else:
                if cargo in self.original:
                    mainCargo = cargo
        itemContext = None if mainCargo is None else Market.getInstance().getCategoryByItem(mainCargo.item).displayName
        menu = ContextMenu.getMenu(self, mainCargo, selection, ("cargoItem", itemContext), ("cargoItemMisc", itemContext))
        if menu:
            self.PopupMenu(menu)

    def getSelectedCargos(self):
        cargos = []
        for row in self.getSelectedRows():
            try:
                cargo = self.cargo[row]
            except IndexError:
                continue
            cargos.append(cargo)
        return cargos

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Total amount of cargo items
        if opt in (1, 2):
            amount = len(fit.cargo)
            return ' ({})'.format(amount) if amount else None
        else:
            return None
