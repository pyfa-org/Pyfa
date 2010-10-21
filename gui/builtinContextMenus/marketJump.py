from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service

class MarketJump(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("module", "ammo", "itemSearch")

    def getText(self, context, selection):
        return "Jump to %s Market Group" % (context.capitalize() if context != "itemSearch" else "Item")

    def activate(self, context, selection, i):
        self.mainFrame.marketBrowser.jump(selection[0])

MarketJump.register()
