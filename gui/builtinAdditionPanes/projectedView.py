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
import gui.globalEvents as GE
from eos.saveddata.drone import Drone as es_Drone
from eos.saveddata.fighter import Fighter as es_Fighter
from eos.saveddata.fit import Fit as es_Fit
from eos.saveddata.module import Module as es_Module
from gui.builtinViewColumns.state import State
from gui.contextMenu import ContextMenu
from gui.utils.staticHelpers import DragDropHelper
from service.fit import Fit
from service.market import Market
import gui.fitCommands as cmd

pyfalog = Logger(__name__)


class DummyItem(object):
    def __init__(self, txt):
        self.name = txt
        self.iconID = None


class DummyEntry(object):
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
    DEFAULT_COLS = ["State",
                    "Ammo Icon",
                    "Base Icon",
                    "Base Name",
                    "Ammo"]

    def __init__(self, parent):
        d.Display.__init__(self, parent, style=wx.LC_SINGLE_SEL | wx.BORDER_NONE)

        self.lastFitId = None

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.Bind(wx.EVT_LEFT_DOWN, self.click)
        self.Bind(wx.EVT_RIGHT_DOWN, self.click)
        self.Bind(wx.EVT_LEFT_DCLICK, self.remove)
        self.Bind(wx.EVT_KEY_UP, self.kbEvent)

        self.droneView = gui.builtinAdditionPanes.droneView.DroneView

        self.Bind(wx.EVT_CONTEXT_MENU, self.spawnMenu)

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)
        self.SetDropTarget(ProjectedViewDrop(self.handleListDrag))

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
            category = Market.getInstance().getItem(itemID, eager=("group.category")).category.name
            if category == 'Module':
                self.mainFrame.command.Submit(cmd.GuiAddProjectedModuleCommand(fitID=fitID, itemID=itemID))
            elif category == 'Drone':
                self.mainFrame.command.Submit(cmd.GuiAddProjectedDroneCommand(fitID=fitID, itemID=itemID))
            elif category == 'Fighter':
                self.mainFrame.command.Submit(cmd.GuiAddProjectedFighterCommand(fitID=fitID, itemID=itemID))

    def kbEvent(self, event):
        keycode = event.GetKeyCode()
        if keycode  in (wx.WXK_DELETE, wx.WXK_NUMPAD_DELETE):
            row = self.GetFirstSelected()
            if row != -1:
                fitID = self.mainFrame.getActiveFit()
                thing = self.get(row)
                if isinstance(thing, es_Fit):
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFitCommand(
                        fitID=fitID, projectedFitID=thing.ID, amount=math.inf))
                elif isinstance(thing, es_Module):
                    fit = Fit.getInstance().getFit(fitID)
                    if thing in fit.projectedModules:
                        position = fit.projectedModules.index(thing)
                        self.mainFrame.command.Submit(cmd.GuiRemoveProjectedModuleCommand(
                            fitID=fitID, position=position))
                elif isinstance(thing, es_Drone):
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedDroneCommand(
                        fitID=fitID, itemID=thing.itemID, amount=math.inf))
                elif isinstance(thing, es_Fighter):
                    fit = Fit.getInstance().getFit(fitID)
                    if thing in fit.projectedFighters:
                        position = fit.projectedFighters.index(thing)
                        self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFighterCommand(
                            fitID=fitID, position=position))

    def handleDrag(self, type, fitID):
        # Those are drags coming from pyfa sources, NOT builtin wx drags
        if type == "fit":
            activeFit = self.mainFrame.getActiveFit()
            if activeFit:
                self.mainFrame.command.Submit(cmd.GuiAddProjectedFitCommand(
                    fitID=activeFit, projectedFitID=fitID, amount=1))

    def startDrag(self, event):
        row = event.GetIndex()
        if row != -1 and isinstance(self.get(row), es_Drone):
            data = wx.TextDataObject()
            dataStr = "projected:" + str(self.GetItemData(row))
            data.SetText(dataStr)

            dropSource = wx.DropSource(self)
            dropSource.SetData(data)
            DragDropHelper.data = dataStr
            dropSource.DoDragDrop()

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

        return (self.droneView.DRONE_ORDER.index(item.marketGroup.name),
                drone.item.name)

    @staticmethod
    def fitSort(fit):
        return fit.name

    def fitChanged(self, event):
        sFit = Fit.getInstance()
        fit = sFit.getFit(event.fitID)
        # pyfalog.debug("ProjectedView::fitChanged: {}", repr(fit))

        self.Parent.Parent.DisablePage(self, not fit or fit.isStructure)

        # Clear list and get out if current fitId is None
        if event.fitID is None and self.lastFitId is not None:
            self.DeleteAllItems()
            self.lastFitId = None
            event.Skip()
            return

        stuff = []
        if fit is not None:
            # pyfalog.debug("    Collecting list of stuff to display in ProjectedView")
            self.fits = fit.projectedFits[:]
            self.modules = fit.projectedModules[:]
            self.drones = fit.projectedDrones[:]
            self.fighters = fit.projectedFighters[:]

            self.fits.sort(key=self.fitSort)
            self.modules.sort(key=self.moduleSort)
            self.drones.sort(key=self.droneSort)
            self.fighters.sort(key=self.fighterSort)

            stuff.extend(self.fits)
            stuff.extend(self.modules)
            stuff.extend(self.drones)
            stuff.extend(self.fighters)

        if event.fitID != self.lastFitId:
            self.lastFitId = event.fitID

            item = self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)

            if item != -1:
                self.EnsureVisible(item)

            self.unselectAll()

        if not stuff:
            stuff = [DummyEntry("Drag an item or fit, or use right-click menu for wormhole effects")]

        self.update(stuff)

        event.Skip()

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
            stuff = self.fits[row]
        elif row - numFits < numMods:
            stuff = self.modules[row - numFits]
        elif row - numFits - numMods < numDrones:
            stuff = self.drones[row - numFits - numMods]
        else:
            stuff = self.fighters[row - numFits - numMods - numDrones]

        return stuff

    def click(self, event):
        event.Skip()
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col == self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                thing = self.get(row)
                button = event.GetButton()
                if isinstance(thing, es_Fit) and button != 3:
                    self.mainFrame.command.Submit(cmd.GuiToggleProjectedFitStateCommand(
                        fitID=fitID, projectedFitID=thing.ID))
                elif isinstance(thing, es_Module):
                    fit = Fit.getInstance().getFit(fitID)
                    if thing in fit.projectedModules:
                        position = fit.projectedModules.index(thing)
                        self.mainFrame.command.Submit(cmd.GuiChangeProjectedModuleStateCommand(
                            fitID=fitID, position=position, click='right' if button == 3 else 'left'))
                elif isinstance(thing, es_Drone) and button != 3:
                    self.mainFrame.command.Submit(cmd.GuiToggleProjectedDroneStateCommand(
                        fitID=fitID, itemID=thing.itemID))
                elif isinstance(thing, es_Fighter) and button != 3:
                    fit = Fit.getInstance().getFit(fitID)
                    if thing in fit.projectedFighters:
                        position = fit.projectedFighters.index(thing)
                        self.mainFrame.command.Submit(cmd.GuiToggleProjectedFighterStatesCommand(
                            fitID=fitID, mainPosition=position, positions=[position]))

    def spawnMenu(self, event):
        fitID = self.mainFrame.getActiveFit()
        if fitID is None:
            return

        if self.getColumn(self.screenToClientFixed(event.Position)) == self.getColIndex(State):
            return

        sel = self.GetFirstSelected()
        context = ()
        item = self.get(sel)

        if item is not None:
            sMkt = Market.getInstance()

            if isinstance(item, es_Drone):
                srcContext = "projectedDrone"
                itemContext = sMkt.getCategoryByItem(item.item).name
                context = ((srcContext, itemContext),)
            elif isinstance(item, es_Fighter):
                srcContext = "projectedFighter"
                itemContext = sMkt.getCategoryByItem(item.item).name
                context = ((srcContext, itemContext),)
            elif isinstance(item, es_Module):
                modSrcContext = "projectedModule"
                modItemContext = sMkt.getCategoryByItem(item.item).name
                modFullContext = (modSrcContext, modItemContext)
                if item.charge is not None:
                    chgSrcContext = "projectedCharge"
                    chgItemContext = sMkt.getCategoryByItem(item.charge).name
                    chgFullContext = (chgSrcContext, chgItemContext)
                    context = (modFullContext, chgFullContext)
                else:
                    context = (modFullContext,)
            else:
                fitSrcContext = "projectedFit"
                fitItemContext = "Fit"
                context = ((fitSrcContext, fitItemContext),)

        context += (("projected",),)
        menu = ContextMenu.getMenu(item, (item,) if item is not None else [], *context)

        if menu is not None:
            self.PopupMenu(menu)

    def remove(self, event):
        row, _ = self.HitTest(event.Position)
        if row != -1:
            col = self.getColumn(event.Position)
            if col != self.getColIndex(State):
                fitID = self.mainFrame.getActiveFit()
                thing = self.get(row)
                if isinstance(thing, es_Fit):
                    amount = math.inf if wx.GetMouseState().altDown else 1
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFitCommand(
                        fitID=fitID, projectedFitID=thing.ID, amount=amount))
                elif isinstance(thing, es_Module):
                    fit = Fit.getInstance().getFit(fitID)
                    if thing in fit.projectedModules:
                        position = fit.projectedModules.index(thing)
                        self.mainFrame.command.Submit(cmd.GuiRemoveProjectedModuleCommand(
                            fitID=fitID, position=position))
                elif isinstance(thing, es_Drone):
                    mstate = wx.GetMouseState()
                    self.mainFrame.command.Submit(cmd.GuiRemoveProjectedDroneCommand(
                        fitID=fitID,
                        itemID=thing.itemID,
                        amount=math.inf if mstate.cmdDown or mstate.altDown else 1))
                elif isinstance(thing, es_Fighter):
                    fit = Fit.getInstance().getFit(fitID)
                    if thing in fit.projectedFighters:
                        position = fit.projectedFighters.index(thing)
                        self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFighterCommand(
                            fitID=fitID, position=position))
