import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit

_t = wx.GetTranslation


class AddToCargo(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ("marketItemGroup", "marketItemMisc"):
            return False

        if mainItem is None:
            return False

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        if not fit or (fit.isStructure and mainItem.category.ID != 8):
            return False

        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Add {} to Cargo").format(itmContext)

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        typeID = int(mainItem.ID)
        command = cmd.GuiAddCargoCommand(fitID=fitID, itemID=typeID, amount=1)
        if self.mainFrame.command.Submit(command):
            self.mainFrame.additionsPane.select("Cargo", focus=False)


AddToCargo.register()
