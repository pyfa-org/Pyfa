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

import gui.builtinAdditionPanes.droneView
import gui.display as d
import gui.fitCommands as cmd
import gui.globalEvents as GE
from gui.builtinContextMenus.commandFitAdd import AddCommandFit
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit


class DummyItem:

    def __init__(self, txt):
        self.name = txt
        self.iconID = None


class DummyEntry:

    def __init__(self, txt):
        self.item = DummyItem(txt)


class CommandViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(CommandViewDrop, self).__init__(*args, **kwargs)
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


class CommandView(d.Display):

    DEFAULT_COLS = ["State", "Base Name"]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, AddCommandFit.fitChanged)
        self.mainFrame.Bind(GE.FIT_REMOVED, self.OnFitRemoved)
        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDoubleClick)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        self.droneView = gui.builtinAdditionPanes.droneView.DroneView

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        self.SetDropTarget(CommandViewDrop(self.handleListDrag))

    def OnFitRemoved(self, event):
        event.Skip()
        AddCommandFit.populateFits(event)
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        self.refreshContents(fit)

    @staticmethod
    def handleListDrag(x, y, data):
        """
        Handles dragging of items from various pyfa displays which support it

        data is list with two indices:
            data[0] is hard-coded str of originating source
            data[1] is typeID or index of data we want to manipulate
        """
        pass

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        mstate = wx.GetMouseState()
        if keycode == wx.WXK_ESCAPE and mstate.GetModifiers() == wx.MOD_NONE:
            self.unselectAll()
        elif keycode == 65 and mstate.GetModifiers() == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and mstate.GetModifiers() == wx.MOD_NONE:
            commandFits = self.getSelectedCommandFits()
            self.removeCommandFits(commandFits)
        event.Skip()

    def handleDrag(self, type, fitID):
        # Those are drags coming from pyfa sources, NOT builtin wx drags
        if type == "fit":
            activeFit = self.mainFrame.getActiveFit()
            if activeFit:
                self.mainFrame.command.Submit(cmd.GuiAddCommandFitCommand(fitID=activeFit, commandFitID=fitID))

    @staticmethod
    def fitSort(fit):
        return fit.name

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and event.fitID is not None and event.fitID != activeFitID:
            return

        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)

        AddCommandFit.populateFits(event)

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if event.fitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            return

        if event.fitID != self.lastFitId:
            self.lastFitId = event.fitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        self.refreshContents(fit)

    def refreshContents(self, fit):
        stuff = []
        if fit is not None:
            self.fits = fit.commandFits[:]
            self.fits.sort(key=self.fitSort)
            stuff.extend(self.fits)
        if not stuff:
            stuff = [DummyEntry("Drag a fit to this area")]
        self.update(stuff)

    def click(self, event):
        mainRow, _ = self.HitTest(event.Position)
        if mainRow != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                try:
                    mainCommandFitID = self.fits[mainRow].ID
                except IndexError:
                    return
                commandFitIDs = []
                for commandFit in self.getSelectedCommandFits():
                    commandFitIDs.append(commandFit.ID)
                if mainCommandFitID not in commandFitIDs:
                    commandFitIDs = [mainCommandFitID]
                self.mainFrame.command.Submit(cmd.GuiToggleCommandFitStatesCommand(
                    fitID=fitID,
                    mainCommandFitID=mainCommandFitID,
                    commandFitIDs=commandFitIDs))
                return
        event.Skip()

    def spawnMenu(self, event):
        selection = self.getSelectedCommandFits()
        clickedPos = self.getRowByAbs(event.Position)
        mainCommandFit = None
        if clickedPos != -1:
            try:
                mainCommandFit = self.fits[clickedPos]
            except IndexError:
                pass
        contexts = []
        if mainCommandFit is not None:
            contexts.append(('commandFit', 'Command Fit'))
        contexts.append(('commandView',))
        menu = ContextMenu.getMenu(mainCommandFit, selection, *contexts)
        if menu:
            self.PopupMenu(menu)

    def onLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            try:
                commandFit = self.fits[row]
            except IndexError:
                return
            self.removeCommandFits([commandFit])

    def removeCommandFits(self, commandFits):
        fitID = self.mainFrame.getActiveFit()
        commandFitIDs = []
        for commandFit in commandFits:
            if commandFit in self.fits:
                commandFitIDs.append(commandFit.ID)
        self.mainFrame.command.Submit(cmd.GuiRemoveCommandFitsCommand(fitID=fitID, commandFitIDs=commandFitIDs))

    def getSelectedCommandFits(self):
        commandFits = []
        for row in self.getSelectedRows():
            try:
                commandFit = self.fits[row]
            except IndexError:
                continue
            commandFits.append(commandFit)
        return commandFits
