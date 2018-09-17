import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
# noinspection PyPackageRequirements
from service.fit import Fit
from service.settings import ContextMenuSettings


class ItemRemove(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('droneRemoveStack'):
            return False

        return srcContext == "droneItem"

    def getText(self, itmContext, selection):
        return "Remove {0} Stack".format(itmContext)

    def activate(self, fullContext, selection, i):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        idx = fit.drones.index(selection[0])
        self.mainFrame.command.Submit(cmd.GuiRemoveDroneCommand(fitID, idx, fit.drones[idx].amount))


ItemRemove.register()
