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
        if not self.settings.get('itemRemove'):
            return False

        return srcContext in ("fittingModule", "droneItem",
                              "implantItem", "boosterItem",
                              "projectedModule", "cargoItem",
                              "projectedFit", "projectedDrone",
                              "fighterItem", "projectedFighter",
                              "commandFit")

    def getText(self, itmContext, selection):
        return u"Remove {0}".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, selection, i):

        srcContext = fullContext[0]
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        if srcContext == "fittingModule":
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalModuleCommand(
                fitID=fitID, modules=[module for module in selection if module is not None]))
        elif srcContext == "fittingCharge":
            self.mainFrame.command.Submit(cmd.GuiChangeLocalModuleChargesCommand(
                fitID=fitID, modules=selection, chargeItemID=None))
        elif srcContext == "droneItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalDroneCommand(
                fitID=fitID, position=fit.drones.index(selection[0]), amount=math.inf))
        elif srcContext == "fighterItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveLocalFighterCommand(
                fitID=fitID, position=fit.fighters.index(selection[0])))
        elif srcContext == "implantItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveImplantCommand(
                fitID=fitID, position=fit.implants.index(selection[0])))
        elif srcContext == "boosterItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveBoosterCommand(
                fitID=fitID, position=fit.boosters.index(selection[0])))
        elif srcContext == "cargoItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveCargoCommand(
                fitID=fitID, itemID=selection[0].itemID))
        elif srcContext == "projectedFit":
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFitCommand(
                fitID=fitID, projectedFitID=selection[0].ID))
        elif srcContext == "projectedModule":
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedModuleCommand(
                fitID=fitID, position=fit.projectedModules.index(selection[0])))
        elif srcContext == "projectedDrone":
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedDroneCommand(
                fitID=fitID, itemID=selection[0].itemID, amount=math.inf))
        elif srcContext == "projectedFighter":
            self.mainFrame.command.Submit(cmd.GuiRemoveProjectedFighterCommand(
                fitID=fitID, position=fit.projectedFighters.index(selection[0])))
        elif srcContext == "commandFit":
            self.mainFrame.command.Submit(cmd.GuiRemoveCommandFitCommand(
                fitID=fitID, commandFitID=selection[0].ID))


RemoveItem.register()
