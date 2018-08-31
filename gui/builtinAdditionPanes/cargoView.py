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
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
import gui.globalEvents as GE
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
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL | wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        self.SetDropTarget(CargoViewDrop(self.handleListDrag))
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)

        if "__WXGTK__" in wx.PlatformInfo:
            self.Bind(wx.EVT_RIGHT_UP, self.scheduleMenu)
        else:
            self.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)

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
            sFit = Fit.getInstance()
            sFit.addCargo(self.mainFrame.getActiveFit(), int(data[1]), 1)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))

    def startDrag(self, event):
        row = event.GetIndex()

        if row != -1:
            data = wx.TextDataObject()
            dataStr = "cargo:" + str(row)
            data.SetText(dataStr)

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            DragDropHelper.data = dataStr
            dropSource.DoDragDrop()

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_NUMPAD_DELETE:
            fitID = self.mainFrame.getActiveFit()
            sFit = Fit.getInstance()
            row = self.GetFirstSelected()
            if row != -1:
                sFit.removeCargo(fitID, self.GetItemData(row))
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
        event.Skip()

    def swapModule(self, x, y, modIdx):
        """Swap a module from fitting window with cargo"""
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.mainFrame.getActiveFit())
        dstRow, _ = self.HitTest((x, y))
        mstate = wx.GetMouseState()

        # Gather module information to get position
        module = fit.modules[modIdx]

        if module.item.isAbyssal:
            dlg = wx.MessageDialog(self,
               "Moving this Abyssal module to the cargo will convert it to the base module. Do you wish to proceed?",
               "Confirm", wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal() == wx.ID_YES

            if not result:
                return

        if dstRow != -1:  # we're swapping with cargo
            if mstate.cmdDown:  # if copying, append to cargo
                sFit.addCargo(self.mainFrame.getActiveFit(), module.item.ID if not module.item.isAbyssal else module.baseItemID)
            else:  # else, move / swap
                sFit.moveCargoToModule(self.mainFrame.getActiveFit(), module.position, dstRow)
        else:  # dragging to blank spot, append
            sFit.addCargo(self.mainFrame.getActiveFit(), module.item.ID if not module.item.isAbyssal else module.baseItemID)

            if not mstate.cmdDown:  # if not copying, remove module
                sFit.removeModule(self.mainFrame.getActiveFit(), module.position)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit(), action="moddel", typeID=module.item.ID))

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)

        # self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if event.fitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            event.Skip()
            return

        self.original = fit.cargo if fit is not None else None
        self.cargo = stuff = fit.cargo if fit is not None else None
        if stuff is not None:
            stuff.sort(key=lambda cargo: cargo.itemID)

        if event.fitID != self.lastFitId:
            self.lastFitId = event.fitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.deselectItems()

        self.populate(stuff)
        self.refresh(stuff)
        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                sFit = Fit.getInstance()
                cargo = self.cargo[self.GetItemData(row)]
                sFit.removeCargo(fitID, self.original.index(cargo))
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def scheduleMenu(self, event):
        event.Skip()
        if self.getColumn(event.Position) != self.getColIndex(State):
            wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        sel = self.GetFirstSelected()
        if sel != -1:
            sFit = Fit.getInstance()
            fit = sFit.getFit(self.mainFrame.getActiveFit())
            cargo = fit.cargo[sel]

            sMkt = Market.getInstance()
            sourceContext = "cargoItem"
            itemContext = sMkt.getCategoryByItem(cargo.item).name

            menu = ContextMenu.getMenu((cargo,), (sourceContext, itemContext))
            self.PopupMenu(menu)
