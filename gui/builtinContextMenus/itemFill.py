import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.settings import ContextMenuSettings


class FillWithItem(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem):
        if not self.settings.get('moduleFill'):
            return False

        if srcContext not in ('marketItemGroup', 'marketItemMisc'):
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        if mainItem.category.name != 'Module':
            return False

        return True

    def getText(self, itmContext, mainItem):
        return "Fill With Module"

    def activate(self, fullContext, mainItem, i):
        self.mainFrame.command.Submit(cmd.GuiFillWithNewLocalModulesCommand(
            fitID=self.mainFrame.getActiveFit(),
            itemID=int(mainItem.ID)))
        self.mainFrame.additionsPane.select('Drones')


FillWithItem.register()
