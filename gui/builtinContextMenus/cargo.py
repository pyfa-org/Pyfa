from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
# noinspection PyPackageRequirements
import wx
from service.fit import Fit


class Cargo(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        fit = sFit.getFit(fitID)
        # Make sure context menu registers in the correct view
        if srcContext not in ("marketItemGroup", "marketItemMisc") or not fit or fit.isStructure:
            return False
        return True

    def getText(self, itmContext, selection):
        return "Add {0} to Cargo".format(itmContext)

    def activate(self, fullContext, selection, i):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        typeID = int(selection[0].ID)
        sFit.addCargo(fitID, typeID)
        self.mainFrame.additionsPane.select("Cargo")
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


Cargo.register()
