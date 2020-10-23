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

_t = wx.GetTranslation

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
        modifiers = event.GetModifiers()
        if keycode == wx.WXK_ESCAPE and modifiers == wx.MOD_NONE:
            self.unselectAll()
        elif keycode == 65 and modifiers == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and modifiers == wx.MOD_NONE:
            commandFits = self.getSelectedCommandFits()
            self.removeCommandFits(commandFits)
        event.Skip()

    def handleDrag(self, type, fitID):
        # Those are drags coming from pyfa sources, NOT builtin wx drags
        if type == "fit":
            activeFit = self.mainFrame.getActiveFit()
            if activeFit:
                self.mainFrame.command.Submit(cmd.GuiAddCommandFitsCommand(fitID=activeFit, commandFitIDs=[fitID]))

    @staticmethod
    def fitSort(fit):
        return fit.name

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

        if activeFitID != self.lastFitId:
            self.lastFitId = activeFitID

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
            stuff = [DummyEntry(_t("Drag a fit to this area"))]
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
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        selection = self.getSelectedCommandFits()
        mainCommandFit = None
        if clickedPos != -1:
            try:
                mainCommandFit = self.fits[clickedPos]
            except IndexError:
                pass
        contexts = []
        if mainCommandFit is not None:
            contexts.append(('commandFit', _t('Command Fit')))
        contexts.append(('commandView',))
        menu = ContextMenu.getMenu(self, mainCommandFit, selection, *contexts)
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

    # Context menu handlers
    def addFit(self, fit):
        if fit is None:
            return
        self.mainFrame.command.Submit(cmd.GuiAddCommandFitsCommand(
            fitID=self.mainFrame.getActiveFit(),
            commandFitIDs=[fit.ID]))

    def getExistingFitIDs(self):
        return [f.ID for f in self.fits]

    def addFitsByIDs(self, fitIDs):
        if not fitIDs:
            return
        self.mainFrame.command.Submit(cmd.GuiAddCommandFitsCommand(
            fitID=self.mainFrame.getActiveFit(),
            commandFitIDs=fitIDs))

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Amount of active command fits
        if opt == 1:
            amount = 0
            for commandFit in fit.commandFits:
                info = commandFit.getCommandInfo(fitID)
                if info is not None and info.active:
                    amount += 1
            return ' ({})'.format(amount) if amount else None
        # Total amount of command fits
        elif opt == 2:
            amount = len(fit.commandFits)
            return ' ({})'.format(amount) if amount else None
        else:
            return None
