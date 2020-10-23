import math

import wx

import gui.fitCommands as cmd
import gui.mainFrame
from eos.saveddata.drone import Drone as EosDrone
from eos.saveddata.fighter import Fighter as EosFighter
from eos.saveddata.fit import Fit as EosFit
from eos.saveddata.module import Module as EosModule
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import getSimilarFighters, getSimilarModPositions
from service.fit import Fit

_t = wx.GetTranslation


class RemoveItem(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem, selection):
        if srcContext not in (
                "fittingModule", "droneItem",
                "implantItem", "boosterItem",
                "projectedModule", "cargoItem",
                "projectedFit", "projectedDrone",
                "fighterItem", "projectedFighter",
                "commandFit", "graphFitList",
                "graphTgtList"
        ):
            return False

        if mainItem is None or getattr(mainItem, "isEmpty", False):
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext, mainItem, selection):
        return _t('Remove {item}{stack}').format(
                item=itmContext if itmContext is not None else _t('Item'),
                stack=_t(' Stack') if self.srcContext in ('droneItem', 'projectedDrone', 'cargoItem', 'projectedFit') else '')

    def activate(self, callingWindow, fullContext, mainItem, selection, i):
        handlerMap = {
            'fittingModule': self.__handleModule,
            'droneItem': self.__handleDrone,
            'fighterItem': self.__handleFighter,
            'implantItem': self.__handleImplant,
            'boosterItem': self.__handleBooster,
            'cargoItem': self.__handleCargo,
            'projectedFit': self.__handleProjectedItem,
            'projectedModule': self.__handleProjectedItem,
            'projectedDrone': self.__handleProjectedItem,
            'projectedFighter': self.__handleProjectedItem,
            'commandFit': self.__handleCommandFit,
            'graphFitList': self.__handleGraphItem,
            'graphTgtList': self.__handleGraphItem
        }
        srcContext = fullContext[0]
        handler = handlerMap.get(srcContext)
        if handler is None:
            return
        handler(callingWindow, mainItem, selection)

    def __handleModule(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
            positions = getSimilarModPositions(fit.modules, mainItem)
        else:
            positions = []
            for mod in selection:
                if mod in fit.modules:
                    positions.append(fit.modules.index(mod))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalModuleCommand(
                fitID=fitID, positions=positions))

    def __handleDrone(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        positions = []
        for drone in selection:
            if drone in fit.drones:
                positions.append(fit.drones.index(drone))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalDronesCommand(
                fitID=fitID, positions=positions, amount=math.inf))

    def __handleFighter(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
            fighters = getSimilarFighters(fit.fighters, mainItem)
        else:
            fighters = selection
        positions = []
        for fighter in fighters:
            if fighter in fit.fighters:
                positions.append(fit.fighters.index(fighter))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalFightersCommand(
                fitID=fitID, positions=positions))

    def __handleImplant(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        positions = []
        for implant in selection:
            if implant in fit.implants:
                positions.append(fit.implants.index(implant))
        self.mainFrame.command.Submit(cmd.GuiRemoveImplantsCommand(
                fitID=fitID, positions=positions))

    def __handleBooster(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        positions = []
        for booster in selection:
            if booster in fit.boosters:
                positions.append(fit.boosters.index(booster))
        self.mainFrame.command.Submit(cmd.GuiRemoveBoostersCommand(
                fitID=fitID, positions=positions))

    def __handleCargo(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        itemIDs = [c.itemID for c in selection]
        self.mainFrame.command.Submit(cmd.GuiRemoveCargosCommand(
                fitID=fitID, itemIDs=itemIDs))

    def __handleProjectedItem(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        if isinstance(mainItem, EosFit):
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                    fitID=fitID, items=selection, amount=math.inf))
        elif isinstance(mainItem, EosModule):
            if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
                fit = Fit.getInstance().getFit(fitID)
                positions = getSimilarModPositions(fit.projectedModules, mainItem)
                items = [fit.projectedModules[p] for p in positions]
            else:
                items = selection
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                    fitID=fitID, items=items, amount=math.inf))
        elif isinstance(mainItem, EosDrone):
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                    fitID=fitID, items=selection, amount=math.inf))
        elif isinstance(mainItem, EosFighter):
            if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
                fit = Fit.getInstance().getFit(fitID)
                items = getSimilarFighters(fit.projectedFighters, mainItem)
            else:
                items = selection
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                    fitID=fitID, items=items, amount=math.inf))
        else:
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedItemsCommand(
                    fitID=fitID, items=selection, amount=math.inf))

    def __handleCommandFit(self, callingWindow, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        commandFitIDs = [cf.ID for cf in selection]
        self.mainFrame.command.Submit(cmd.GuiRemoveCommandFitsCommand(
                fitID=fitID, commandFitIDs=commandFitIDs))

    def __handleGraphItem(self, callingWindow, mainItem, selection):
        callingWindow.removeWrappers(selection)


RemoveItem.register()
