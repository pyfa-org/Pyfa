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

import gui.globalEvents as GE
import gui.mainFrame
from gui.builtinMarketBrowser.events import ItemSelected, ITEM_SELECTED
from gui.display import Display
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market


class DroneViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(DroneViewDrop, self).__init__(*args, **kwargs)
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


class DroneView(Display):
    DEFAULT_COLS = [
        "State",
        # "Base Icon",
        "Base Name",
        # "prop:droneDps,droneBandwidth",
        "Max Range",
        "Miscellanea",
        "attr:maxVelocity",
        "Price",
    ]

    def __init__(self, parent):
        Display.__init__(self, parent, style=wx.LC_SINGLE_SEL | wx.BORDER_NONE)

        self.lastFitId = None

        self.hoveredRow = None
        self.hoveredColumn = None

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.removeItem)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        if "__WXGTK__" in wx.PlatformInfo:
            self.Bind(wx.EVT_RIGHT_UP, self.scheduleMenu)
        else:
            self.Bind(wx.EVT_RIGHT_DOWN, self.scheduleMenu)

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)
        self.SetDropTarget(DroneViewDrop(self.handleDragDrop))

    def OnLeaveWindow(self, event):
        self.SetToolTip(None)
        self.hoveredRow = None
        self.hoveredColumn = None
        event.Skip()

    def OnMouseMove(self, event):
        row, _, col = self.HitTestSubItem(event.Position)
        if row != self.hoveredRow or col != self.hoveredColumn:
            if self.ToolTip is not None:
                self.SetToolTip(None)
            else:
                self.hoveredRow = row
                self.hoveredColumn = col
                if row != -1 and col != -1 and col < len(self.DEFAULT_COLS):
                    mod = self.drones[self.GetItemData(row)]
                    if self.DEFAULT_COLS[col] == "Miscellanea":
                        tooltip = self.activeColumns[col].getToolTip(mod)
                        if tooltip is not None:
                            self.SetToolTip(tooltip)
                        else:
                            self.SetToolTip(None)
                    else:
                        self.SetToolTip(None)
                else:
                    self.SetToolTip(None)
        event.Skip()

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_NUMPAD_DELETE:
            row = self.GetFirstSelected()
            if row != -1:
                drone = self.drones[self.GetItemData(row)]
                self.removeDrone(drone)

        event.Skip()

    def startDrag(self, event):
        row = event.GetIndex()
        if row != -1:
            data = wx.TextDataObject()
            dataStr = "drone:" + str(row)
            data.SetText(dataStr)

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            DragDropHelper.data = dataStr
            dropSource.DoDragDrop()

    def handleDragDrop(self, x, y, data):
        """
        Handles dragging of items from various pyfa displays which support it

        data is list with two indices:
            data[0] is hard-coded str of originating source
            data[1] is typeID or index of data we want to manipulate
        """
        if data[0] == "drone":  # we want to merge drones
            srcRow = int(data[1])
            dstRow, _ = self.HitTest((x, y))
            if srcRow != -1 and dstRow != -1:
                self._merge(srcRow, dstRow)
        elif data[0] == "market":
            wx.PostEvent(self.mainFrame, ItemSelected(itemID=int(data[1])))

    def _merge(self, src, dst):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        if sFit.mergeDrones(fitID, self.drones[src], self.drones[dst]):
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    DRONE_ORDER = ('Light Scout Drones', 'Medium Scout Drones',
                   'Heavy Attack Drones', 'Sentry Drones', 'Fighters',
                   'Fighter Bombers', 'Combat Utility Drones',
                   'Electronic Warfare Drones', 'Logistic Drones', 'Mining Drones', 'Salvage Drones')

    def droneKey(self, drone):
        sMkt = Market.getInstance()

        groupName = sMkt.getMarketGroupByItem(drone.item).name

        return (self.DRONE_ORDER.index(groupName),
                drone.item.name)

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

        self.original = fit.drones if fit is not None else None
        self.drones = stuff = fit.drones[:] if fit is not None else None

        if stuff is not None:
            stuff.sort(key=self.droneKey)

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
            event.Skip()
            return

        trigger = sFit.addDrone(fitID, event.itemID)
        if trigger:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
            self.mainFrame.additionsPane.select("Drones")

        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                drone = self.drones[self.GetItemData(row)]
                self.removeDrone(drone)

    def removeDrone(self, drone):
        fitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        sFit.removeDrone(fitID, self.original.index(drone))
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def click(self, event):
        event.Skip()
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                sFit = Fit.getInstance()
                drone = self.drones[row]
                sFit.toggleDrone(fitID, self.original.index(drone))
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def scheduleMenu(self, event):
        event.Skip()
        if self.getColumn(event.Position) != self.getColIndex(State):
            wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        sel = self.GetFirstSelected()
        if sel != -1:
            drone = self.drones[sel]

            sMkt = Market.getInstance()
            sourceContext = "droneItem"
            itemContext = sMkt.getCategoryByItem(drone.item).name
            menu = ContextMenu.getMenu((drone,), (sourceContext, itemContext))
            self.PopupMenu(menu)
