from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import wx
import gui.globalEvents as GE

class ItemRemove(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        return srcContext in ("fittingModule", "fittingCharge", "droneItem", "implantItem", "boosterItem", "projectedModule", "projectedCharge",
                               "projectedFit", "projectedDrone")

    def getText(self, itmContext, selection):
        return "Remove {0}".format(itmContext if itmContext is not None else "Item")

    def activate(self, fullContext, selection, i):
        srcContext = fullContext[0]
        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        if srcContext == "fittingModule":
            for module in selection:
                if module is not None:
                    sFit.removeModule(fitID,fit.modules.index(module))
        elif srcContext in ("fittingCharge" , "projectedCharge"):
            sFit.setAmmo(fitID, None, selection)
        elif srcContext == "droneItem":
            sFit.removeDrone(fitID, fit.drones.index(selection[0]))
        elif srcContext == "implantItem":
            sFit.removeImplant(fitID, fit.implants.index(selection[0]))
        elif srcContext == "boosterItem":
            sFit.removeBooster(fitID, fit.boosters.index(selection[0]))
        else:
            sFit.removeProjected(fitID, selection[0])

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))




ItemRemove.register()
