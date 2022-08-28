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


DRONE_ORDER = ('Light Scout Drones', 'Medium Scout Drones',
               'Heavy Attack Drones', 'Sentry Drones', 'Combat Utility Drones',
               'Electronic Warfare Drones', 'Logistic Drones', 'Mining Drones', 'Salvage Drones')


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
        "Drone HP",
        "Drone Regen",
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
        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDoubleClick)
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
                        mod = self.drones[row]
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
        modifiers = event.GetModifiers()
        if keycode == wx.WXK_ESCAPE and modifiers == wx.MOD_NONE:
            self.unselectAll()
        elif keycode == 65 and modifiers == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and modifiers == wx.MOD_NONE:
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
            if srcRow != -1:
                if wx.GetMouseState().GetModifiers() == wx.MOD_CONTROL:
                    try:
                        srcDrone = self.drones[srcRow]
                    except IndexError:
                        return
                    if srcDrone not in self.original:
                        return
                    self.mainFrame.command.Submit(cmd.GuiCloneLocalDroneCommand(
                        fitID=self.mainFrame.getActiveFit(),
                        position=self.original.index(srcDrone)))
                else:
                    dstRow, _ = self.HitTest((x, y))
                    if dstRow != -1:
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

    @staticmethod
    def droneKey(drone):
        groupName = Market.getInstance().getMarketGroupByItem(drone.item).marketGroupName
        return (DRONE_ORDER.index(groupName), drone.isMutated, drone.fullName)

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

        self.original = fit.drones if fit is not None else None
        self.drones = fit.drones[:] if fit is not None else None

        if self.drones is not None:
            self.drones.sort(key=self.droneKey)

        if activeFitID != self.lastFitId:
            self.lastFitId = activeFitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.update(self.drones)

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

        amount = droneStackLimit(fit, event.itemID) if wx.GetMouseState().GetModifiers() == wx.MOD_ALT else 1
        if self.mainFrame.command.Submit(cmd.GuiAddLocalDroneCommand(fitID=fitID, itemID=event.itemID, amount=amount)):
            self.mainFrame.additionsPane.select('Drones')

        event.Skip()

    def onLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                try:
                    drone = self.drones[row]
                except IndexError:
                    return
                if event.GetModifiers() == wx.MOD_ALT:
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
                    if mainPosition not in positions:
                        positions = [mainPosition]
                    self.mainFrame.command.Submit(cmd.GuiToggleLocalDroneStatesCommand(
                        fitID=self.mainFrame.getActiveFit(),
                        mainPosition=mainPosition,
                        positions=positions))
                    return
        event.Skip()

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        mainDrone = None
        if clickedPos != -1:
            try:
                drone = self.drones[clickedPos]
            except IndexError:
                pass
            else:
                if drone in self.original:
                    mainDrone = drone
        selection = self.getSelectedDrones()
        itemContext = None if mainDrone is None else Market.getInstance().getCategoryByItem(mainDrone.item).displayName
        menu = ContextMenu.getMenu(self, mainDrone, selection, ("droneItem", itemContext), ("droneItemMisc", itemContext))
        if menu:
            self.PopupMenu(menu)

    def getSelectedDrones(self):
        drones = []
        for row in self.getSelectedRows():
            try:
                drone = self.drones[row]
            except IndexError:
                continue
            drones.append(drone)
        return drones

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Amount of active drones
        if opt == 1:
            amount = 0
            for droneStack in fit.drones:
                amount += droneStack.amountActive
            return ' ({})'.format(amount) if amount else None
        # Total amount of drones
        elif opt == 2:
            amount = 0
            for droneStack in fit.drones:
                amount += droneStack.amount
            return ' ({})'.format(amount) if amount else None
        else:
            return None
