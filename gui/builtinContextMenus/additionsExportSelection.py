import gui.mainFrame
from gui.contextMenu import ContextMenuSelection
from gui.utils.clipboard import toClipboard
from service.fit import Fit
from service.port.eft import exportDrones, exportFighters, exportCargo, exportImplants, exportBoosters


viewSpecMap = {
    'droneItemMisc': ('Drones', exportDrones),
    'fighterItemMisc': ('Fighters', exportFighters),
    'cargoItemMisc': ('Cargo Items', exportCargo),
    'implantItemMisc': ('Implants', exportImplants),
    'implantItemMiscChar': ('Implants', exportImplants),
    'boosterItemMisc': ('Boosters', exportBoosters)}


class AdditionsExportAll(ContextMenuSelection):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, selection):
        if srcContext not in viewSpecMap:
            return False
        if not selection:
            return False
        fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
        if fit is None:
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext, selection):
        return 'Copy Selected {}'.format(viewSpecMap[self.srcContext][0])

    def activate(self, callingWindow, fullContext, selection, i):
        export = viewSpecMap[self.srcContext][1](selection)
        if export:
            toClipboard(export)


AdditionsExportAll.register()
