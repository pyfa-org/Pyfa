import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.settings import ContextMenuSettings


class AddToCargoAmmo(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem):
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        if mainItem.category.ID != 8:
            return False

        return True

    def getText(self, itmContext, mainItem):
        return "Add {0} to Cargo (x1000)".format(itmContext)

    def activate(self, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        typeID = int(mainItem.ID)
        self.mainFrame.command.Submit(cmd.GuiAddCargoCommand(
            fitID=fitID, itemID=typeID, amount=1000))
        self.mainFrame.additionsPane.select("Cargo")


AddToCargoAmmo.register()
