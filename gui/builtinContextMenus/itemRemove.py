from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.fit import Fit
from service.settings import ContextMenuSettings


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
        return "Remove {0}".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, selection, i):

        srcContext = fullContext[0]
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        if srcContext == "fittingModule":
            for module in selection:
                if module is not None:
                    sFit.removeModule(fitID, fit.modules.index(module))
        elif srcContext in ("fittingCharge", "projectedCharge"):
            sFit.setAmmo(fitID, None, selection)
        elif srcContext == "droneItem":
            sFit.removeDrone(fitID, fit.drones.index(selection[0]))
        elif srcContext == "fighterItem":
            sFit.removeFighter(fitID, fit.fighters.index(selection[0]))
        elif srcContext == "implantItem":
            sFit.removeImplant(fitID, fit.implants.index(selection[0]))
        elif srcContext == "boosterItem":
            sFit.removeBooster(fitID, fit.boosters.index(selection[0]))
        elif srcContext == "cargoItem":
            sFit.removeCargo(fitID, fit.cargo.index(selection[0]))
        elif srcContext in ("projectedFit", "projectedModule", "projectedDrone", "projectedFighter"):
            sFit.removeProjected(fitID, selection[0])
        elif srcContext == "commandFit":
            sFit.removeCommand(fitID, selection[0])

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


ItemRemove.register()
