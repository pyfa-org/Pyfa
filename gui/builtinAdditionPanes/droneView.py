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


import math

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
import gui.fitCommands as cmd
from gui.fitCommands.helpers import droneStackLimit


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
        Display.__init__(self, parent, style=wx.BORDER_NONE)

        self.lastFitId = None

        self.hoveredRow = None
        self.hoveredColumn = None

        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

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
                    try:
                        mod = self.drones[self.GetItemData(row)]
                    except IndexError:
                        return
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
        mstate = wx.GetMouseState()
        if keycode == wx.WXK_ESCAPE and not mstate.cmdDown and not mstate.altDown and not mstate.shiftDown:
            self.unselectAll()
        if keycode == 65 and mstate.cmdDown and not mstate.altDown and not mstate.shiftDown:
            self.selectAll()
        if keycode == wx.WXK_DELETE or keycode == wx.WXK_NUMPAD_DELETE:
            drones = self.getSelectedDrones()
            self.removeDroneStacks(drones)
        event.Skip()

    def startDrag(self, event):
        row = event.GetIndex()
        if row != -1:
            self.unselectAll()
            self.Select(row, True)

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
        if data[0] == "drone":
            srcRow = int(data[1])
            dstRow, _ = self.HitTest((x, y))
            if srcRow != -1 and dstRow != -1:
                self._merge(srcRow, dstRow)
        elif data[0] == "market":
            wx.PostEvent(self.mainFrame, ItemSelected(itemID=int(data[1])))

    def _merge(self, srcRow, dstRow):
        fitID = self.mainFrame.getActiveFit()
        try:
            srcDrone = self.drones[srcRow]
            dstDrone = self.drones[dstRow]
        except IndexError:
            return
        if srcDrone in self.original and dstDrone in self.original:
            srcPosition = self.original.index(srcDrone)
            dstPosition = self.original.index(dstDrone)
            self.mainFrame.command.Submit(cmd.GuiMergeLocalDroneStacksCommand(
                fitID=fitID, srcPosition=srcPosition, dstPosition=dstPosition))

    DRONE_ORDER = ('Light Scout Drones', 'Medium Scout Drones',
                   'Heavy Attack Drones', 'Sentry Drones', 'Combat Utility Drones',
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
        self.drones = fit.drones[:] if fit is not None else None

        if self.drones is not None:
            self.drones.sort(key=self.droneKey)

        if event.fitID != self.lastFitId:
            self.lastFitId = event.fitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.update(self.drones)
        event.Skip()

    def addItem(self, event):
        item = Market.getInstance().getItem(event.itemID, eager='group.category')
        if item is None or not item.isDrone:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if not fit or fit.isStructure:
            event.Skip()
            return

        amount = droneStackLimit(fit, event.itemID) if wx.GetMouseState().altDown else 1
        if self.mainFrame.command.Submit(cmd.GuiAddLocalDroneCommand(fitID=fitID, itemID=event.itemID, amount=amount)):
            self.mainFrame.additionsPane.select('Drones')

        event.Skip()

    def OnLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                mstate = wx.GetMouseState()
                try:
                    drone = self.drones[self.GetItemData(row)]
                except IndexError:
                    return
                if mstate.cmdDown or mstate.altDown:
                    self.removeDroneStacks([drone])
                else:
                    self.removeDrone(drone)

    def removeDrone(self, drone):
        fitID = self.mainFrame.getActiveFit()
        if drone in self.original:
            position = self.original.index(drone)
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalDronesCommand(
                fitID=fitID, positions=[position], amount=1))

    def removeDroneStacks(self, drones):
        fitID = self.mainFrame.getActiveFit()
        positions = []
        for drone in drones:
            if drone in self.original:
                positions.append(self.original.index(drone))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalDronesCommand(
            fitID=fitID, positions=positions, amount=math.inf))

    def click(self, event):
        mainRow, _ = self.HitTest(event.Position)
        if mainRow != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                try:
                    mainDrone = self.drones[mainRow]
                except IndexError:
                    return
                if mainDrone in self.original:
                    mainPosition = self.original.index(mainDrone)
                    positions = []
                    for row in self.getSelectedRows():
                        try:
                            drone = self.drones[row]
                        except IndexError:
                            continue
                        if drone in self.original:
                            positions.append(self.original.index(drone))
                    self.mainFrame.command.Submit(cmd.GuiToggleLocalDroneStatesCommand(
                        fitID=fitID,
                        mainPosition=mainPosition,
                        positions=positions))
                    return
        event.Skip()

    def spawnMenu(self, event):
        selection = self.getSelectedDrones()
        clickedPos = self.getRowByAbs(event.Position)
        mainDrone = None
        if clickedPos != -1:
            try:
                drone = self.drones[clickedPos]
            except IndexError:
                pass
            else:
                if drone in self.original:
                    mainDrone = drone
        sourceContext = "droneItem"
        itemContext = None if mainDrone is None else Market.getInstance().getCategoryByItem(mainDrone.item).name
        menu = ContextMenu.getMenu(mainDrone, selection, (sourceContext, itemContext))
        if menu:
            self.PopupMenu(menu)

    def getSelectedDrones(self):
        drones = []
        for row in self.getSelectedRows():
            try:
                drone = self.drones[self.GetItemData(row)]
            except IndexError:
                continue
            drones.append(drone)
        return drones
