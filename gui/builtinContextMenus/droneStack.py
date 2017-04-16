from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
import wx
from service.settings import ContextMenuSettings
from service.fit import Fit


class DroneStack(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('droneStack'):
            return False

        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        for selected_item in selection:
            if selected_item.category.ID in (
                    18,  # Drones
            ):
                return True

        return False

    def getText(self, itmContext, selection):
        return "Add {0} to Drone Bay (x5)".format(itmContext)

    def activate(self, fullContext, selection, i):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        typeID = int(selection[0].ID)
        sFit.addDrone(fitID, typeID, 5)
        self.mainFrame.additionsPane.select("Drones")
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


DroneStack.register()
