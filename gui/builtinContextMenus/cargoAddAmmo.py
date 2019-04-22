import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings


class AddToCargoAmmo(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        for selected_item in selection:
            if selected_item.category.ID in (
                    8,  # Charge
            ):
                return True

    def getText(self, itmContext, mainItem, selection):
        return "Add {0} to Cargo (x1000)".format(itmContext)

    def activate(self, fullContext, mainItem, selection, i):
        fitID = self.mainFrame.getActiveFit()
        typeID = int(selection[0].ID)
        self.mainFrame.command.Submit(cmd.GuiAddCargoCommand(
            fitID=fitID, itemID=typeID, amount=1000))
        self.mainFrame.additionsPane.select("Cargo")


AddToCargoAmmo.register()
