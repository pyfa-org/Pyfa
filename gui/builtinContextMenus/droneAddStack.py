import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import droneStackLimit
from service.fit import Fit
from service.settings import ContextMenuSettings


class DroneAddStack(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if srcContext not in ('marketItemGroup', 'marketItemMisc'):
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        if mainItem.category.name != 'Drone':
            return False

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        amount = droneStackLimit(fit, mainItem)
        if amount < 1:
            return False

        self.amount = amount
        return True

    def getText(self, itmContext, mainItem, selection):
        return 'Add {} to Drone Bay{}'.format(
            itmContext, '' if self.amount == 1 else ' (x{})'.format(self.amount))

    def activate(self, fullContext, mainItem, selection, i):
        self.mainFrame.command.Submit(cmd.GuiAddLocalDroneCommand(
            fitID=self.mainFrame.getActiveFit(),
            itemID=int(mainItem.ID),
            amount=self.amount))
        self.mainFrame.additionsPane.select('Drones')


DroneAddStack.register()
