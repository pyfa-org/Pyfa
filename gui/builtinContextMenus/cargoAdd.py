import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit
from service.settings import ContextMenuSettings


class AddToCargo(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem):
        if srcContext not in ("marketItemGroup", "marketItemMisc"):
            return False

        if mainItem is None:
            return False

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)
        # Make sure context menu registers in the correct view
        if not fit or fit.isStructure:
            return False

        return True

    def getText(self, itmContext, mainItem):
        return "Add {} to Cargo".format(itmContext)

    def activate(self, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()

        typeID = int(mainItem.ID)

        self.mainFrame.command.Submit(cmd.GuiAddCargoCommand(
            fitID=fitID, itemID=typeID, amount=1))
        self.mainFrame.additionsPane.select("Cargo")


AddToCargo.register()
