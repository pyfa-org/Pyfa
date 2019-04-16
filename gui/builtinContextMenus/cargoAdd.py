import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class AddToCargo(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('cargo'):
            return False

        if srcContext not in ("marketItemGroup", "marketItemMisc"):
            return False

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        # Make sure context menu registers in the correct view
        if not fit or fit.isStructure:
            return False

        return True

    def getText(self, itmContext, selection):
        return "Add {} to Cargo".format(itmContext)

    def activate(self, fullContext, selection, i):
        fitID = self.mainFrame.getActiveFit()

        typeID = int(selection[0].ID)

        self.mainFrame.command.Submit(cmd.GuiAddCargoCommand(fitID, typeID, 1))
        self.mainFrame.additionsPane.select("Cargo")


AddToCargo.register()
