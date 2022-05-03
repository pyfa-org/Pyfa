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
from service.port import Port
from service.port.esi import ESIExportException


_t = wx.GetTranslation

class CartViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(CartViewDrop, self).__init__(*args, **kwargs)
        self.dropFn = dropFn
        #this is really transferring an EVE itemID
        self.dropData = wx.TextDataObject()
        self.SetDataObject(self.dropData)

    def OnData(self, x, y, t):
        if self.GetData():
            dragged_data = DragDropHelper.data
            data = dragged_data.split(':')
            self.dropFn(x, y, data)
        return t


class CartView(d.Display):
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
            self.SetDropTarget(CartViewDrop(self.handleListDrag))
            self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)

            self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)





        def addItem(self, event):
            newFit = "cartBackGroundFit.xml"
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
            self.mainFrame.command.Submit(cmd.GuiAddCartCommand(
                fitID=fitID, itemID=item.ID, amount=amount))
            self.mainFrame.additionsPane.select('Cart')
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
                    self.mainFrame.command.Submit(cmd.GuiAddCartCommand(
                        fitID=fitID, itemID=int(data[1]), amount=1))

        def startDrag(self, event):
            row = event.GetIndex()

            if row != -1:
                data = wx.TextDataObject()
                try:
                    dataStr = "cart:{}".format(self.cart[row].itemID)
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
                carts = self.getSelectedCarts()
                self.removeCarts(carts)
            event.Skip()

        def swapModule(self, x, y, modIdx):
            """Swap a module from fitting window with carts"""
            sFit = Fit.getInstance()
            fit = sFit.getFit(self.mainFrame.getActiveFit())
            dstRow, _ = self.HitTest((x, y))

            if dstRow > -1:
                try:
                    dstCartsItemID = getattr(self.cart[dstRow], 'itemID', None)
                except IndexError:
                    dstCartsItemID = None
            else:
                dstCartsItemID = None

            self.mainFrame.command.Submit(cmd.GuiLocalModuleToCartCommand(
                fitID=self.mainFrame.getActiveFit(),
                modPosition=modIdx,
                cartItemID=dstCartsItemID,
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

            self.original = fit.cart if fit is not None else None
            self.cart = fit.cart[:] if fit is not None else None
            if self.cart is not None:
                self.cart.sort(key=lambda c: (c.item.group.category.name, c.item.group.name, c.item.name))

            if activeFitID != self.lastFitId:
                self.lastFitId = activeFitID

                item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

                if item != -1:
                    self.EnsureVisible(item)

                self.unselectAll()

            self.populate(self.cart)
            self.refresh(self.cart)

        def onLeftDoubleClick(self, event):
            row, _ = self.HitTest(event.Position)
            if row != -1:
                try:
                    cart = self.cart[row]
                except IndexError:
                    return
                self.removeCarts([cart])

        def removeCarts(self, carts):
            fitID = self.mainFrame.getActiveFit()
            itemIDs = []
            for cart in carts:
                if cart in self.original:
                    itemIDs.append(cart.itemID)
            self.mainFrame.command.Submit(cmd.GuiRemoveCartCommand(fitID=fitID, itemIDs=itemIDs))

        def spawnMenu(self, event):
            clickedPos = self.getRowByAbs(event.Position)
            self.ensureSelection(clickedPos)

            selection = self.getSelectedCarts()
            mainCart = None
            if clickedPos != -1:
                try:
                    cart = self.cart[clickedPos]
                except IndexError:
                    pass
                else:
                    if cart in self.original:
                        mainCart = cart
            itemContext = None if mainCart is None else Market.getInstance().getCategoryByItem(
                mainCart.item).displayName
            menu = ContextMenu.getMenu(self, mainCart, selection, ("cartItem", itemContext),
                                       ("cartItemMisc", itemContext))
            if menu:
                self.PopupMenu(menu)

        def getSelectedCarts(self):
            carts = []
            for row in self.getSelectedRows():
                try:
                    cart = self.cart[row]
                except IndexError:
                    continue
                carts.append(cart)
            return carts

        def getTabExtraText(self):
            fitID = self.mainFrame.getActiveFit()
            if fitID is None:
                return None
            sFit = Fit.getInstance()
            fit = sFit.getFit(fitID)
            if fit is None:
                return None
            opt = sFit.serviceFittingOptions["additionsLabels"]
            # Total amount of cart items
            if opt in (1, 2):
                amount = len(fit.cart)
                return ' ({})'.format(amount) if amount else None
            else:
                return None
