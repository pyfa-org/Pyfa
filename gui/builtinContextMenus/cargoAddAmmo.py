import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle

_t = wx.GetTranslation


class AddToCargoAmmo(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ("marketItemGroup", "marketItemMisc") or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        if mainItem.category.ID != 8:
            return False

        return True

    def getText(self, callingWindow, itmContext, mainItem):
        if mainItem.marketGroup.name == "Scan Probes":
            return _t("Add {0} to Cargo (x8)").format(itmContext)
        return _t("Add a variable amount of {0} to cargo").format(itmContext)

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        typeID = int(mainItem.ID)

        if mainItem.marketGroup.name == "Scan Probes":
            command = cmd.GuiAddCargoCommand(fitID=fitID, itemID=typeID, amount=8)
        else:
            quantity_to_add = wx.TextEntryDialog(None, "How many would you like to add to cargo",
                                                 'Quantity', 'number')
            if quantity_to_add.ShowModal() == wx.ID_OK:
                quantity = int(quantity_to_add.GetValue())
            else:
                quantity = 0
            command = cmd.GuiAddCargoCommand(fitID=fitID, itemID=typeID, amount=quantity)
        
        if self.mainFrame.command.Submit(command):
            self.mainFrame.additionsPane.select("Cargo", focus=False)


AddToCargoAmmo.register()
