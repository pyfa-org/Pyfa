import math

import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import getSimilarModPositions, getSimilarFighters
from service.fit import Fit
from service.settings import ContextMenuSettings


class RemoveItem(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if srcContext not in (
            "fittingModule", "droneItem",
            "implantItem", "boosterItem",
            "projectedModule", "cargoItem",
            "projectedFit", "projectedDrone",
            "fighterItem", "projectedFighter",
            "commandFit"
        ):
            return False

        if mainItem is None or getattr(mainItem, "isEmpty", False):
            return False

        return True

    def getText(self, itmContext, mainItem, selection):
        return 'Remove {}{}'.format(
            itmContext if itmContext is not None else 'Item',
            ' Stack' if itmContext in ('Drone', 'Fit') else '')

    def activate(self, fullContext, mainItem, selection, i):
        handlerMap = {
            'fittingModule': self.__handleModule,
            'droneItem': self.__handleDrone,
            'fighterItem': self.__handleFighter,
            'implantItem': self.__handleImplant,
            'boosterItem': self.__handleBooster,
            'cargoItem': self.__handleCargo,
            'projectedFit': self.__handleProjectedFit,
            'projectedModule': self.__handleProjectedModule,
            'projectedDrone': self.__handleProjectedDrone,
            'projectedFighter': self.__handleProjectedFighter,
            'commandFit': self.__handleCommandFit}
        srcContext = fullContext[0]
        handler = handlerMap.get(srcContext)
        if handler is None:
            return
        handler(mainItem, selection)

    def __handleModule(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().altDown:
            positions = getSimilarModPositions(fit.modules, mainItem)
        else:
            positions = []
            for mod in selection:
                if mod in fit.modules:
                    positions.append(fit.modules.index(mod))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalModuleCommand(
            fitID=fitID, positions=positions))

    def __handleDrone(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        positions = []
        for drone in selection:
            if drone in fit.drones:
                positions.append(fit.drones.index(drone))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalDronesCommand(
            fitID=fitID, positions=positions, amount=math.inf))

    def __handleFighter(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if wx.GetMouseState().altDown:
            fighters = getSimilarFighters(fit.fighters, mainItem)
        else:
            fighters = selection
        positions = []
        for fighter in fighters:
            if fighter in fit.fighters:
                positions.append(fit.fighters.index(fighter))
        self.mainFrame.command.Submit(cmd.GuiRemoveLocalFightersCommand(
            fitID=fitID, positions=positions))

    def __handleImplant(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mainItem in fit.implants:
            position = fit.implants.index(mainItem)
            self.mainFrame.command.Submit(cmd.GuiRemoveImplantCommand(
                fitID=fitID, position=position))

    def __handleBooster(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mainItem in fit.boosters:
            position = fit.boosters.index(mainItem)
            self.mainFrame.command.Submit(cmd.GuiRemoveBoosterCommand(
                fitID=fitID, position=position))

    def __handleCargo(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        itemIDs = [c.itemID for c in selection]
        self.mainFrame.command.Submit(cmd.GuiRemoveCargosCommand(
            fitID=fitID, itemIDs=itemIDs))

    def __handleProjectedFit(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFitCommand(
            fitID=fitID, projectedFitID=mainItem.ID, amount=math.inf))

    def __handleProjectedModule(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mainItem in fit.projectedModules:
            position = fit.projectedModules.index(mainItem)
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedModuleCommand(
                fitID=fitID, position=position))

    def __handleProjectedDrone(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        self.mainFrame.command.Submit(cmd.GuiRemoveProjectedDroneCommand(
            fitID=fitID, itemID=mainItem.itemID, amount=math.inf))

    def __handleProjectedFighter(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mainItem in fit.projectedFighters:
            position = fit.projectedFighters.index(mainItem)
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFighterCommand(
                fitID=fitID, position=position))

    def __handleCommandFit(self, mainItem, selection):
        fitID = self.mainFrame.getActiveFit()
        self.mainFrame.command.Submit(cmd.GuiRemoveCommandFitCommand(
            fitID=fitID, commandFitID=mainItem.ID))


RemoveItem.register()
