import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle

_t = wx.GetTranslation


class FillWithItem(ContextMenuSingle):
    visibilitySetting = 'moduleFill'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ('marketItemGroup', 'marketItemMisc'):
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        if mainItem.category.name != 'Module':
            return False

        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Fill With Module")

    def activate(self, callingWindow, fullContext, mainItem, i):
        self.mainFrame.command.Submit(cmd.GuiFillWithNewLocalModulesCommand(
                fitID=self.mainFrame.getActiveFit(),
                itemID=int(mainItem.ID)))


FillWithItem.register()
