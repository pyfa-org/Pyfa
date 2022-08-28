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
import gui.mainFrame
from eos.const import FittingSlot
from gui.builtinMarketBrowser.events import ItemSelected, ITEM_SELECTED
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.fitCommands.helpers import getSimilarFighters
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market


FIGHTER_ORDER = ('Light Fighter', 'Heavy Fighter', 'Support Fighter')
_t = wx.GetTranslation


class FighterViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(FighterViewDrop, self).__init__(*args, **kwargs)
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


class FighterView(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, style=wx.TAB_TRAVERSAL)
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.labels = [("Light", _t("Light")), ("Heavy", _t("Heavy")), ("Support", _t("Support"))]

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.fighterDisplay = FighterDisplay(self)
        mainSizer.Add(self.fighterDisplay, 1, wx.EXPAND, 0)

        textSizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer.AddStretchSpacer()

        for attr, label in self.labels:
            lbl = wx.StaticText(self, wx.ID_ANY, label)
            textSizer.Add(lbl, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            lbl = wx.StaticText(self, wx.ID_ANY, "0")
            setattr(self, "label%sUsed" % attr, lbl)
            textSizer.Add(lbl, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

            textSizer.Add(wx.StaticText(self, wx.ID_ANY, "/"), 0, wx.ALIGN_CENTER)

            lbl = wx.StaticText(self, wx.ID_ANY, "0")
            setattr(self, "label%sTotal" % attr, lbl)
            textSizer.Add(lbl, 0, wx.ALIGN_CENTER)
            textSizer.AddStretchSpacer()

        mainSizer.Add(textSizer, 0, wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)

        if fit:
            for x, _ in self.labels:
                if fit.isStructure:
                    slot = getattr(FittingSlot, "FS_{}".format(x.upper()))
                else:
                    slot = getattr(FittingSlot, "F_{}".format(x.upper()))
                used = fit.getSlotsUsed(slot)
                total = fit.getNumSlots(slot)
                color = wx.Colour(204, 51, 51) if used > total else wx.SystemSettings.GetColour(
                    wx.SYS_COLOUR_WINDOWTEXT)

                lbl = getattr(self, "label%sUsed" % x.capitalize())
                lbl.SetLabel(str(int(used)))
                lbl.SetForegroundColour(color)

                lbl = getattr(self, "label%sTotal" % x.capitalize())
                lbl.SetLabel(str(int(total)))
                lbl.SetForegroundColour(color)

            self.Refresh()

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Amount of active fighter squads
        if opt == 1:
            amount = len([f for f in fit.fighters if f.active])
            return ' ({})'.format(amount) if amount else None
        # Total amount of fighter squads
        elif opt == 2:
            amount = len(fit.fighters)
            return ' ({})'.format(amount) if amount else None
        else:
            return None


class FighterDisplay(d.Display):

    DEFAULT_COLS = ["State",
                    # "Base Icon",
                    "Base Name",
                    # "prop:droneDps,droneBandwidth",
                    # "Max Range",
                    # "Miscellanea",
                    "attr:maxVelocity",
                    "Drone HP",
                    "Drone Regen",
                    "Fighter Abilities",
                    "Price",
                    ]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.BORDER_NONE)

        self.lastFitId = None

        self.hoveredRow = None
        self.hoveredColumn = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(ITEM_SELECTED, self.addItem)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

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
                    try:
                        mod = self.fighters[row]
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
            fighters = self.getSelectedFighters()
            self.removeFighters(fighters)
        event.Skip()

    def startDrag(self, event):
        row = event.GetIndex()
        if row != -1:
            self.unselectAll()
            self.Select(row, True)

            data = wx.TextDataObject()
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

    @staticmethod
    def fighterKey(fighter):
        groupName = Market.getInstance().getGroupByItem(fighter.item).name
        orderPos = FIGHTER_ORDER.index(groupName)
        # Sort support fighters by name, ignore their abilities
        if groupName == 'Support Fighter':
            abilityEffectIDs = ()
        # Group up fighters from various roles
        else:
            abilityEffectIDs = sorted(a.effectID for a in fighter.abilities)
        return orderPos, abilityEffectIDs, fighter.item.name

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(activeFitID)

        self.Parent.Parent.Parent.DisablePage(self.Parent, not fit)

        # Clear list and get out if current fitId is None
        if activeFitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            return

        self.original = fit.fighters if fit is not None else None
        self.fighters = fit.fighters[:] if fit is not None else None

        if self.fighters is not None:
            self.fighters.sort(key=self.fighterKey)

        if activeFitID != self.lastFitId:
            self.lastFitId = activeFitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.update(self.fighters)

    def addItem(self, event):
        item = Market.getInstance().getItem(event.itemID, eager='group.category')
        if item is None or not item.isFighter:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        if self.mainFrame.command.Submit(cmd.GuiAddLocalFighterCommand(fitID, event.itemID)):
            self.mainFrame.additionsPane.select('Fighters')

        event.Skip()

    def onLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                try:
                    fighter = self.fighters[row]
                except IndexError:
                    return
                if event.GetModifiers() == wx.MOD_ALT:
                    fighters = getSimilarFighters(self.original, fighter)
                else:
                    fighters = [fighter]
                self.removeFighters(fighters)

    def removeFighters(self, fighters):
        fitID = self.mainFrame.getActiveFit()
        positions = []
        for fighter in fighters:
            if fighter in self.original:
                positions.append(self.original.index(fighter))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalFightersCommand(fitID=fitID, positions=positions))

    def click(self, event):
        mainRow, _ = self.HitTest(event.Position)
        if mainRow != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                try:
                    mainFighter = self.fighters[mainRow]
                except IndexError:
                    return
                if mainFighter in self.original:
                    mainPosition = self.original.index(mainFighter)
                    positions = []
                    if event.GetModifiers() == wx.MOD_ALT:
                        for fighter in getSimilarFighters(self.original, mainFighter):
                            positions.append(self.original.index(fighter))
                    else:
                        for row in self.getSelectedRows():
                            try:
                                fighter = self.fighters[row]
                            except IndexError:
                                continue
                            if fighter in self.original:
                                positions.append(self.original.index(fighter))
                    if mainPosition not in positions:
                        positions = [mainPosition]
                    self.mainFrame.command.Submit(cmd.GuiToggleLocalFighterStatesCommand(
                        fitID=fitID,
                        mainPosition=mainPosition,
                        positions=positions))
                    return
        event.Skip()

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        selection = self.getSelectedFighters()
        mainFighter = None
        if clickedPos != -1:
            try:
                fighter = self.fighters[clickedPos]
            except IndexError:
                pass
            else:
                if fighter in self.original:
                    mainFighter = fighter
        itemContext = None if mainFighter is None else Market.getInstance().getCategoryByItem(mainFighter.item).displayName
        menu = ContextMenu.getMenu(self, mainFighter, selection, ("fighterItem", itemContext), ("fighterItemMisc", itemContext))
        if menu:
            self.PopupMenu(menu)

    def getSelectedFighters(self):
        fighters = []
        for row in self.getSelectedRows():
            try:
                fighter = self.fighters[row]
            except IndexError:
                continue
            fighters.append(fighter)
        return fighters
