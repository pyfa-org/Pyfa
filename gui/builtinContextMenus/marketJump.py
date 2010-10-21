from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service

class MarketJump(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("module", "ammo", "itemSearch", "drone", "implant", "booster") \
               and (not selection[0].isEmpty if context == "module" else True)

    def getText(self, context, selection):
        return "Jump to %s Market Group" % (context.capitalize() if context != "itemSearch" else "Item")

    def activate(self, context, selection, i):
        if context in ("module", "drone", "implant", "booster"):
            item = selection[0].item
        elif context == "ammo":
            item = selection[0].charge
        else:
            item = selection[0]

        self.mainFrame.marketBrowser.jump(item)

MarketJump.register()
