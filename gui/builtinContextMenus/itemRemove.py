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

        srcContext = fullContext[0]
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        if srcContext == "fittingModule":
            if wx.GetMouseState().altDown:
                positions = getSimilarModPositions(fit.modules, mainItem)
            else:
                positions = []
                for mod in selection:
                    if mod in fit.modules:
                        positions.append(fit.modules.index(mod))
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalModuleCommand(
                fitID=fitID, positions=positions))
        elif srcContext == "droneItem":
            positions = []
            for drone in selection:
                if drone in fit.drones:
                    positions.append(fit.drones.index(drone))
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalDronesCommand(
                fitID=fitID, positions=positions, amount=math.inf))
        elif srcContext == "fighterItem":
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
        elif srcContext == "implantItem":
            if mainItem in fit.implants:
                position = fit.implants.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiRemoveImplantCommand(
                    fitID=fitID, position=position))
        elif srcContext == "boosterItem":
            if mainItem in fit.boosters:
                position = fit.boosters.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiRemoveBoosterCommand(
                    fitID=fitID, position=position))
        elif srcContext == "cargoItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveCargosCommand(
                fitID=fitID, itemIDs=[mainItem.itemID]))
        elif srcContext == "projectedFit":
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFitCommand(
                fitID=fitID, projectedFitID=mainItem.ID, amount=math.inf))
        elif srcContext == "projectedModule":
            if mainItem in fit.projectedModules:
                position = fit.projectedModules.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiRemoveProjectedModuleCommand(
                    fitID=fitID, position=position))
        elif srcContext == "projectedDrone":
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedDroneCommand(
                fitID=fitID, itemID=mainItem.itemID, amount=math.inf))
        elif srcContext == "projectedFighter":
            if mainItem in fit.projectedFighters:
                position = fit.projectedFighters.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFighterCommand(
                    fitID=fitID, position=position))
        elif srcContext == "commandFit":
            self.mainFrame.command.Submit(cmd.GuiRemoveCommandFitCommand(
                fitID=fitID, commandFitID=mainItem.ID))


RemoveItem.register()
