import math

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class RemoveItem(ContextMenu):

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

        if mainItem is None and len(selection) == 0:
            return False

        return True

    def getText(self, itmContext, mainItem, selection):
        return 'Remove {}{}'.format(
            itmContext if itmContext is not None else 'Item',
            ' Stack' if itmContext in ('Drone', 'Fit') else '')

    def activate(self, fullContext, mainItem, selection, i):

        mainItem = selection[0] if mainItem is None else mainItem

        srcContext = fullContext[0]
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        if srcContext == "fittingModule":
            positions = []
            for position, mod in enumerate(fit.modules):
                if mod in selection:
                    positions.append(position)
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalModuleCommand(
                fitID=fitID, positions=positions))
        elif srcContext == "droneItem":
            if mainItem in fit.drones:
                position = fit.drones.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiRemoveLocalDroneCommand(
                    fitID=fitID, position=position, amount=math.inf))
        elif srcContext == "fighterItem":
            if mainItem in fit.fighters:
                position = fit.fighters.index(mainItem)
                self.mainFrame.command.Submit(cmd.GuiRemoveLocalFighterCommand(
                    fitID=fitID, position=position))
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
            self.mainFrame.command.Submit(cmd.GuiRemoveCargoCommand(
                fitID=fitID, itemID=mainItem.itemID))
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
