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
from logbook import Logger

import gui.builtinAdditionPanes.droneView
import gui.display as d
import gui.fitCommands as cmd
import gui.globalEvents as GE
from eos.const import FittingModuleState
from eos.saveddata.drone import Drone as EosDrone
from eos.saveddata.fighter import Fighter as EosFighter
from eos.saveddata.fit import Fit as EosFit
from eos.saveddata.module import Module as EosModule
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.fitCommands.helpers import getSimilarFighters, getSimilarModPositions
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)
_t = wx.GetTranslation

class DummyItem:
    def __init__(self, txt):
        self.name = txt
        self.iconID = None


class DummyEntry:
    def __init__(self, txt):
        self.item = DummyItem(txt)


class ProjectedViewDrop(wx.DropTarget):
    def __init__(self, dropFn, *args, **kwargs):
        super(ProjectedViewDrop, self).__init__(*args, **kwargs)
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


class ProjectedView(d.Display):
    DEFAULT_COLS = ['State',
                    'Ammo Icon',
                    'Base Icon',
                    'Base Name',
                    'Ammo',
                    'Projection Range']

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(GE.FIT_REMOVED, self.OnFitRemoved)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.click)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onLeftDoubleClick)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        self.SetDropTarget(ProjectedViewDrop(self.handleListDrag))

    def OnFitRemoved(self, event):
        event.Skip()
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        self.refreshContents(fit)

    def handleListDrag(self, x, y, data):
        """
        Handles dragging of items from various pyfa displays which support it

        data is list with two indices:
            data[0] is hard-coded str of originating source
            data[1] is typeID or index of data we want to manipulate
        """
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if data[0] == 'fitting':
            dstRow, _ = self.HitTest((x, y))
            # Gather module information to get position
            self.mainFrame.command.Submit(cmd.GuiAddProjectedModuleCommand(
                fitID=fitID, itemID=fit.modules[int(data[1])].itemID))
        elif data[0] == 'market':
            itemID = int(data[1])
            item = Market.getInstance().getItem(itemID)
            if item.isModule:
                self.mainFrame.command.Submit(cmd.GuiAddProjectedModuleCommand(fitID=fitID, itemID=itemID))
            elif item.isDrone:
                self.mainFrame.command.Submit(cmd.GuiAddProjectedDroneCommand(fitID=fitID, itemID=itemID))
            elif item.isFighter:
                self.mainFrame.command.Submit(cmd.GuiAddProjectedFighterCommand(fitID=fitID, itemID=itemID))

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()
        if keycode == wx.WXK_ESCAPE and modifiers == wx.MOD_NONE:
            self.unselectAll()
        elif keycode == 65 and modifiers == wx.MOD_CONTROL:
            self.selectAll()
        elif keycode in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE) and modifiers == wx.MOD_NONE:
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                fitID=self.mainFrame.getActiveFit(),
                items=self.getSelectedProjectors(),
                amount=math.inf))
        event.Skip()

    def handleDrag(self, type, fitID):
        # Those are drags coming from pyfa sources, NOT builtin wx drags
        if type == 'fit':
            activeFit = self.mainFrame.getActiveFit()
            if activeFit:
                self.mainFrame.command.Submit(cmd.GuiAddProjectedFitsCommand(
                    fitID=activeFit, projectedFitIDs=[fitID], amount=1))

    @staticmethod
    def moduleSort(module):
        return not module.isExclusiveSystemEffect, module.item.name

    @staticmethod
    def fighterSort(fighter):
        return fighter.item.name

    def droneSort(self, drone):
        item = drone.item
        if item.marketGroup is None:
            item = item.metaGroup.parent

        return (gui.builtinAdditionPanes.droneView.DRONE_ORDER.index(item.marketGroup.name),
                drone.item.name)

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
        # pyfalog.debug('ProjectedView::fitChanged: {}', repr(fit))

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
            self.originalFits = fit.projectedFits
            self.fits = fit.projectedFits[:]
            self.originalModules = fit.projectedModules
            self.modules = fit.projectedModules[:]
            self.originalDrones = fit.projectedDrones
            self.drones = fit.projectedDrones[:]
            self.originalFighters = fit.projectedFighters
            self.fighters = fit.projectedFighters[:]

            self.fits.sort(key=self.fitSort)
            self.modules.sort(key=self.moduleSort)
            self.drones.sort(key=self.droneSort)
            self.fighters.sort(key=self.fighterSort)

            stuff.extend(self.fits)
            stuff.extend(self.modules)
            stuff.extend(self.drones)
            stuff.extend(self.fighters)
        if not stuff:
            stuff = [DummyEntry(_t('Drag an item or fit, or use right-click menu for wormhole effects'))]
        self.update(stuff)

    def get(self, row):
        if row == -1:
            return None

        numFits = len(self.fits)
        numMods = len(self.modules)
        numDrones = len(self.drones)
        numFighters = len(self.fighters)

        if (numFits + numMods + numDrones + numFighters) == 0:
            return None

        if row < numFits:
            fit = self.fits[row]
            if fit in self.originalFits:
                return fit
        elif row - numFits < numMods:
            mod = self.modules[row - numFits]
            if mod in self.originalModules:
                return mod
        elif row - numFits - numMods < numDrones:
            drone = self.drones[row - numFits - numMods]
            if drone in self.originalDrones:
                return drone
        else:
            fighter = self.fighters[row - numFits - numMods - numDrones]
            if fighter in self.originalFighters:
                return fighter
        return None

    def click(self, event):
        mainRow, _ = self.HitTest(event.Position)
        if mainRow != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                mainItem = self.get(mainRow)
                if mainItem is None:
                    return
                selection = self.getSelectedProjectors()
                if mainItem not in selection:
                    selection = [mainItem]
                modPressed = event.GetModifiers() == wx.MOD_ALT
                fitID = self.mainFrame.getActiveFit()
                if isinstance(mainItem, EosModule) and modPressed:
                    fit = Fit.getInstance().getFit(fitID)
                    positions = getSimilarModPositions(fit.projectedModules, mainItem)
                    selection = [fit.projectedModules[p] for p in positions]
                elif isinstance(mainItem, EosFighter) and modPressed:
                    fit = Fit.getInstance().getFit(fitID)
                    selection = getSimilarFighters(fit.projectedFighters, mainItem)
                self.mainFrame.command.Submit(cmd.GuiChangeProjectedItemStatesCommand(
                    fitID=fitID,
                    mainItem=mainItem,
                    items=selection,
                    click='right' if event.GetButton() == 3 else 'left'))
                return
        event.Skip()

    def spawnMenu(self, event):
        clickedPos = self.getRowByAbs(event.Position)
        self.ensureSelection(clickedPos)

        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return

        if self.getColumn(self.screenToClientFixed(event.Position)) == self.getColIndex(State):
            return

        mainItem = self.get(clickedPos)

        contexts = []
        if mainItem is not None:
            sMkt = Market.getInstance()

            if isinstance(mainItem, EosModule):
                modSrcContext = 'projectedModule'
                modItemContext = _t('Projected Item')
                modFullContext = (modSrcContext, modItemContext)
                contexts.append(modFullContext)
                if mainItem.charge is not None:
                    chargeSrcContext = 'projectedCharge'
                    chargeItemContext = sMkt.getCategoryByItem(mainItem.charge).displayName
                    chargeFullContext = (chargeSrcContext, chargeItemContext)
                    contexts.append(chargeFullContext)
            elif isinstance(mainItem, EosDrone):
                srcContext = 'projectedDrone'
                itemContext = _t('Projected Item')
                droneFullContext = (srcContext, itemContext)
                contexts.append(droneFullContext)
            elif isinstance(mainItem, EosFighter):
                srcContext = 'projectedFighter'
                itemContext = _t('Projected Item')
                fighterFullContext = (srcContext, itemContext)
                contexts.append(fighterFullContext)
            else:
                fitSrcContext = 'projectedFit'
                fitItemContext = _t('Projected Item')
                fitFullContext = (fitSrcContext, fitItemContext)
                contexts.append(fitFullContext)
        contexts.append(('projected',))

        selection = self.getSelectedProjectors()
        menu = ContextMenu.getMenu(self, mainItem, selection, *contexts)
        if menu is not None:
            self.PopupMenu(menu)

    def onLeftDoubleClick(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                mainItem = self.get(row)
                if mainItem is None:
                    return
                fitID = self.mainFrame.getActiveFit()
                modPressed = event.GetModifiers() == wx.MOD_ALT
                if isinstance(mainItem, EosFit):
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                        fitID=fitID, items=[mainItem], amount=math.inf if modPressed else 1))
                elif isinstance(mainItem, EosModule):
                    if modPressed:
                        fit = Fit.getInstance().getFit(fitID)
                        positions = getSimilarModPositions(fit.projectedModules, mainItem)
                        items = [fit.projectedModules[p] for p in positions]
                    else:
                        items = [mainItem]
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                        fitID=fitID, items=items, amount=1))
                elif isinstance(mainItem, EosDrone):
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                        fitID=fitID, items=[mainItem], amount=math.inf if modPressed else 1))
                elif isinstance(mainItem, EosFighter):
                    if modPressed:
                        fit = Fit.getInstance().getFit(fitID)
                        items = getSimilarFighters(fit.projectedFighters, mainItem)
                    else:
                        items = [mainItem]
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                        fitID=fitID, items=items, amount=1))
                else:
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                        fitID=fitID, items=[mainItem], amount=math.inf if modPressed else 1))

    def getSelectedProjectors(self):
        projectors = []
        for row in self.getSelectedRows():
            projector = self.get(row)
            if projector is None:
                continue
            projectors.append(projector)
        return projectors

    # Context menu handlers
    def addFit(self, fit):
        if fit is None:
            return
        self.mainFrame.command.Submit(cmd.GuiAddProjectedFitsCommand(
            fitID=self.mainFrame.getActiveFit(),
            projectedFitIDs=[fit.ID],
            amount=1))

    def getExistingFitIDs(self):
        return [f.ID for f in self.fits]

    def addFitsByIDs(self, fitIDs):
        if not fitIDs:
            return
        self.mainFrame.command.Submit(cmd.GuiAddProjectedFitsCommand(
            fitID=self.mainFrame.getActiveFit(),
            projectedFitIDs=fitIDs,
            amount=1))

    def getTabExtraText(self):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return None
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        if fit is None:
            return None
        opt = sFit.serviceFittingOptions["additionsLabels"]
        # Amount of active projected items
        if opt == 1:
            amount = 0
            for projectedFit in fit.projectedFits:
                info = projectedFit.getProjectionInfo(fitID)
                if info is not None and info.active:
                    amount += 1
            amount += len([m for m in fit.projectedModules if m.state > FittingModuleState.OFFLINE])
            amount += len([d for d in fit.projectedDrones if d.amountActive > 0])
            amount += len([f for f in fit.projectedFighters if f.active])
            return ' ({})'.format(amount) if amount else None
        # Total amount of projected items
        elif opt == 2:
            amount = 0
            amount += len(fit.projectedFits)
            amount += len(fit.projectedModules)
            amount += len(fit.projectedDrones)
            amount += len(fit.projectedFighters)
            return ' ({})'.format(amount) if amount else None
        else:
            return None
