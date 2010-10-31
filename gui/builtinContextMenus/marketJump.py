from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service

class MarketJump(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("module", "ammo", "itemSearch", "drone", "implant", "booster", "projectedModule", "projectedDrone") \
               and (not selection[0].isEmpty if context == "module" else True)

    REPLACES = {"itemSearch": "Item",
                "projectedModule": "Module",
                "projectedDrone": "Drone"}

    def getText(self, context, selection):
        return "Jump to %s Market Group" % (context.capitalize() if context not in self.REPLACES else self.REPLACES[context])

    def activate(self, context, selection, i):
        if context in ("module", "drone", "implant", "booster", "projectedModule", "projectedDrone"):
            item = selection[0].item
        elif context in ("ammo", "projectedAmmo"):
            item = selection[0].charge
        else:
            item = selection[0]

        self.mainFrame.marketBrowser.jump(item)
        self.mainFrame.notebookBrowsers.SetSelection(0)

MarketJump.register()
