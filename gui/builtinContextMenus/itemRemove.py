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

    def display(self, srcContext, selection):
        return srcContext in ("fittingModule", "droneItem",
                              "implantItem", "boosterItem",
                              "projectedModule", "cargoItem",
                              "projectedFit", "projectedDrone",
                              "fighterItem", "projectedFighter",
                              "commandFit")

    def getText(self, itmContext, selection):
        return 'Remove {}{}'.format(
            itmContext if itmContext is not None else 'Item',
            ' Stack' if itmContext == 'Drone' else '')

    def activate(self, fullContext, selection, i):

        srcContext = fullContext[0]
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        if srcContext == "fittingModule":
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalModuleCommand(
                fitID=fitID, modules=[module for module in selection if module is not None]))
        elif srcContext == "droneItem":
            drone = selection[0]
            if drone in fit.drones:
                position = fit.drones.index(drone)
                self.mainFrame.command.Submit(cmd.GuiRemoveLocalDroneCommand(
                    fitID=fitID, position=position, amount=math.inf))
        elif srcContext == "fighterItem":
            fighter = selection[0]
            if fighter in fit.fighters:
                position = fit.fighters.index(fighter)
                self.mainFrame.command.Submit(cmd.GuiRemoveLocalFighterCommand(
                    fitID=fitID, position=position))
        elif srcContext == "implantItem":
            implant = selection[0]
            if implant in fit.implants:
                position = fit.implants.index(implant)
                self.mainFrame.command.Submit(cmd.GuiRemoveImplantCommand(
                    fitID=fitID, position=position))
        elif srcContext == "boosterItem":
            booster = selection[0]
            if booster in fit.boosters:
                position = fit.boosters.index(booster)
                self.mainFrame.command.Submit(cmd.GuiRemoveBoosterCommand(
                    fitID=fitID, position=position))
        elif srcContext == "cargoItem":
            cargo = selection[0]
            self.mainFrame.command.Submit(cmd.GuiRemoveCargoCommand(
                fitID=fitID, itemID=cargo.itemID))
        elif srcContext == "projectedFit":
            projectedFit = selection[0]
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFitCommand(
                fitID=fitID, projectedFitID=projectedFit.ID))
        elif srcContext == "projectedModule":
            mod = selection[0]
            if mod in fit.projectedModules:
                position = fit.projectedModules.index(mod)
                self.mainFrame.command.Submit(cmd.GuiRemoveProjectedModuleCommand(
                    fitID=fitID, position=position))
        elif srcContext == "projectedDrone":
            drone = selection[0]
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedDroneCommand(
                fitID=fitID, itemID=drone.itemID, amount=math.inf))
        elif srcContext == "projectedFighter":
            fighter = selection[0]
            if fighter in fit.projectedFighters:
                position = fit.projectedFighters.index(fighter)
                self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFighterCommand(
                    fitID=fitID, position=position))
        elif srcContext == "commandFit":
            commandFit = selection[0]
            self.mainFrame.command.Submit(cmd.GuiRemoveCommandFitCommand(
                fitID=fitID, commandFitID=commandFit.ID))


RemoveItem.register()
