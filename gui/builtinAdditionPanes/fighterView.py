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
from gui.builtinMarketBrowser.events import ItemSelected, ITEM_SELECTED
import gui.mainFrame
import gui.display as d
from gui.builtinViewColumns.state import State
from eos.saveddata.module import Slot
from gui.contextMenu import ContextMenu
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market


class FighterViewDrop(wx.PyDropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(FighterViewDrop, self).__init__(*args, **kwargs)
        self.dropFn = dropFn
        # this is really transferring an EVE itemID
        self.dropData = wx.PyTextDataObject()
        self.SetDataObject(self.dropData)

    def OnData(self, x, y, t):
        if self.GetData():
            dragged_data = DragDropHelper.data
            data = dragged_data.split(':')
            self.dropFn(x, y, data)
        return t


class FighterView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.labels = ["Light", "Heavy", "Support"]

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.fighterDisplay = FighterDisplay(self)
        mainSizer.Add(self.fighterDisplay, 1, wx.EXPAND, 0)

        textSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        for x in self.labels:
            lbl = wx.StaticText(self, wx.ID_ANY, x.capitalize())
            textSizer.Add(lbl, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            lbl = wx.StaticText(self, wx.ID_ANY, "0")
            setattr(self, "label%sUsed" % (x.capitalize()), lbl)
            textSizer.Add(lbl, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            textSizer.Add(wx.StaticText(self, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(self, wx.ID_ANY, "0")
            setattr(self, "label%sTotal" % (x.capitalize()), lbl)
            textSizer.Add(lbl, 0, wx.ALIGN_CENTER)
            textSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        mainSizer.Add(textSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        activeFitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(activeFitID)

        if fit:
            for x in self.labels:
                slot = getattr(Slot, "F_{}".format(x.upper()))
                used = fit.getSlotsUsed(slot)
                total = fit.getNumSlots(slot)
                color = wx.Colour(204, 51, 51) if used > total else wx.SystemSettings_GetColour(
                    wx.SYS_COLOUR_WINDOWTEXT)

                lbl = getattr(self, "label%sUsed" % x.capitalize())
                lbl.SetLabel(str(int(used)))
                lbl.SetForegroundColour(color)

                lbl = getattr(self, "label%sTotal" % x.capitalize())
                lbl.SetLabel(str(int(total)))
                lbl.SetForegroundColour(color)

            self.Refresh()


class FighterDisplay(d.Display):
    DEFAULT_COLS = ["State",
                    # "Base Icon",
                    "Base Name",
                    # "prop:droneDps,droneBandwidth",
                    # "Max Range",
                    # "Miscellanea",
                    "attr:maxVelocity",
                    "Fighter Abilities"
                    # "Price",
                    ]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL | wx.BORDER_NONE)

        self.lastFitId = None

        self.hoveredRow = None
        self.hoveredColumn = None

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
        self.SetDropTarget(FighterViewDrop(self.handleDragDrop))

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
                    mod = self.fighters[self.GetItemData(row)]
                    if self.DEFAULT_COLS[col] == "Miscellanea":
                        tooltip = self.activeColumns[col].getToolTip(mod)
                        if tooltip is not None:
                            self.SetToolTipString(tooltip)
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
                fighter = self.fighters[self.GetItemData(row)]
                self.removeFighter(fighter)

        event.Skip()

    def startDrag(self, event):
        row = event.GetIndex()
        if row != -1:
            data = wx.PyTextDataObject()
            dataStr = "fighter:" + str(row)
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
        if data[0] == "fighter":  # we want to merge fighters
            srcRow = int(data[1])
            dstRow, _ = self.HitTest((x, y))
            if srcRow != -1 and dstRow != -1:
                self._merge(srcRow, dstRow)
        elif data[0] == "market":
            wx.PostEvent(self.mainFrame, ItemSelected(itemID=int(data[1])))

    @staticmethod
    def _merge(src, dst):
        return

    '''
    DRONE_ORDER = ('Light Scout Drones', 'Medium Scout Drones',
                   'Heavy Attack Drones', 'Sentry Drones', 'Fighters',
                   'Fighter Bombers', 'Combat Utility Drones',
                   'Electronic Warfare Drones', 'Logistic Drones', 'Mining Drones', 'Salvage Drones',
                   'Light Fighters', 'Heavy Fighters', 'Support Fighters')
    def droneKey(self, drone):
        sMkt = Market.getInstance()

        groupName = sMkt.getMarketGroupByItem(drone.item).name
        print groupName
        return (self.DRONE_ORDER.index(groupName),
                drone.item.name)
    '''

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)

        self.Parent.Parent.Parent.DisablePage(self.Parent, not fit)

        # Clear list and get out if current fitId is None
        if event.fitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            event.Skip()
            return

        self.original = fit.fighters if fit is not None else None
        self.fighters = stuff = fit.fighters[:] if fit is not None else None

        '''
        if stuff is not None:
            stuff.sort(key=self.droneKey)
        '''

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
        trigger = sFit.addFighter(fitID, event.itemID)
        if trigger:
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))
            self.mainFrame.additionsPane.select("Fighters")

        event.Skip()

    def removeItem(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                fighter = self.fighters[self.GetItemData(row)]
                self.removeFighter(fighter)

    def removeFighter(self, fighter):
        fitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        sFit.removeFighter(fitID, self.original.index(fighter))
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def click(self, event):
        event.Skip()
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                sFit = Fit.getInstance()
                fighter = self.fighters[row]
                sFit.toggleFighter(fitID, self.original.index(fighter))
                wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def scheduleMenu(self, event):
        event.Skip()
        if self.getColumn(event.Position) != self.getColIndex(State):
            wx.CallAfter(self.spawnMenu)

    def spawnMenu(self):
        sel = self.GetFirstSelected()
        if sel != -1:
            fighter = self.fighters[sel]

            sMkt = Market.getInstance()
            sourceContext = "fighterItem"
            itemContext = sMkt.getCategoryByItem(fighter.item).name
            menu = ContextMenu.getMenu((fighter,), (sourceContext, itemContext))
            self.PopupMenu(menu)
