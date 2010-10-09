from gui.contextMenu import ContextMenu
from gui.itemStats import ItemStatsDialog
from gui.patternEditor import DmgPatternEditorDlg
import gui.mainFrame
import service

class DamagePattern(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        return context in ("resistancesViewFull",)

    def getText(self, context, selection):
        sDP = service.DamagePattern.getInstance()
        return map(lambda p: p.name, sDP.getDamagePatternList())

    def activate(self, context, selection, i):
        dlg=DmgPatternEditorDlg(self.mainFrame)
        dlg.ShowModal()
        dlg.Destroy()
DamagePattern.register()
