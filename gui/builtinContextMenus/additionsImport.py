import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.clipboard import fromClipboard
from service.fit import Fit
from service.port.eft import parseAdditions
from service.settings import ContextMenuSettings


viewSpecMap = {
    'droneItemMisc': ('Drones', None),
    'fighterItemMisc': ('Fighters', None),
    'cargoItemMisc': ('Cargo Items', None),
    'implantItemMisc': ('Implants', None),
    'implantItemMiscChar': ('Implants', None),
    'boosterItemMisc': ('Boosters', None)}


class AdditionsImport(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if not ContextMenuSettings.getInstance().get('additionsCopyPaste'):
            return False
        if srcContext not in viewSpecMap:
            return False
        fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
        if fit is None:
            return False
        if not fromClipboard():
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext):
        return 'Paste {}'.format(viewSpecMap[self.srcContext][0])

    def activate(self, callingWindow, fullContext, i):
        text = fromClipboard()
        items = parseAdditions(text)


AdditionsImport.register()
