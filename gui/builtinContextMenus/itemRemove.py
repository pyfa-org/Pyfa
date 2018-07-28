from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.fit import Fit
from service.settings import ContextMenuSettings
import gui.fitCommands as cmd

class ItemRemove(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('itemRemove'):
            return False

        return srcContext in ("fittingModule", "fittingCharge",
                              "droneItem", "implantItem",
                              "boosterItem", "projectedModule",
                              "projectedCharge", "cargoItem",
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
            modules = [module for module in selection if module is not None]
            self.mainFrame.command.Submit(cmd.GuiModuleRemoveCommand(fitID, modules))
            return  # the command takes care of the PostEvent
        elif srcContext in ("fittingCharge", "projectedCharge"):
            self.mainFrame.command.Submit(cmd.GuiModuleAddChargeCommand(fitID, None, selection))
        elif srcContext == "droneItem":
            sFit.removeDrone(fitID, fit.drones.index(selection[0]))
        elif srcContext == "fighterItem":
            sFit.removeFighter(fitID, fit.fighters.index(selection[0]))
        elif srcContext == "implantItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveImplantCommand(fitID, fit.implants.index(selection[0])))
            return  # the command takes care of the PostEvent
        elif srcContext == "boosterItem":
            sFit.removeBooster(fitID, fit.boosters.index(selection[0]))
        elif srcContext == "cargoItem":
            self.mainFrame.command.Submit(cmd.GuiRemoveCargoCommand(fitID, selection[0].itemID))
            return  # the command takes care of the PostEvent
        elif srcContext in ("projectedFit", "projectedModule", "projectedDrone", "projectedFighter"):
            sFit.removeProjected(fitID, selection[0])
        elif srcContext == "commandFit":
            sFit.removeCommand(fitID, selection[0])

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


ItemRemove.register()
