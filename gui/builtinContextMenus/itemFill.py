import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings


class FillWithItem(ContextMenu):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if not self.settings.get('moduleFill'):
            return False
        if srcContext not in ('marketItemGroup', 'marketItemMisc'):
            return False
        if self.mainFrame.getActiveFit() is None:
            return False
        item = selection[0]
        if item.category.name != 'Module':
            return False
        return True

    def getText(self, itmContext, mainItem, selection):
        return "Fill With Module"

    def activate(self, fullContext, mainItem, selection, i):
        self.mainFrame.command.Submit(cmd.GuiFillWithNewLocalModulesCommand(
            fitID=self.mainFrame.getActiveFit(),
            itemID=int(selection[0].ID)))
        self.mainFrame.additionsPane.select('Drones')


FillWithItem.register()
