from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service

class ItemStats(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("item", "ship", "module", "ammo", "skill")

    def getText(self, context, selection):
        return "%s stats" % context.capitalize()

    def activate(self, context, selection, i):
        if context == "ship":
            fitID = self.mainFrame.getActiveFit()
            cFit = service.Fit.getInstance()
            stuff = cFit.getFit(fitID).ship
        elif context == "ammo":
            stuff = selection[0].charge
        else:
            stuff = selection[0]

        if context == "module" and stuff.isEmpty:
            return

        dlg=ItemStatsDialog(stuff, context)

ItemStats.register()
