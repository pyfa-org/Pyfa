from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
import gui.mainFrame
import service

class DamagePattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("resistancesViewFull",)

    def getText(self, context, selection):
        return "%s stats" % context.capitalize()

    def activate(self, context, selection, i):
        pass

DamagePattern.register()
