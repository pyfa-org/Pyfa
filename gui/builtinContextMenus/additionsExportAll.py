import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.clipboard import toClipboard
from service.fit import Fit
from service.port.eft import exportDrones, exportFighters, exportCargo, exportImplants, exportBoosters
from service.settings import ContextMenuSettings


viewSpecMap = {
    'droneItemMisc': ('Drones', lambda cw: cw.drones, exportDrones),
    'fighterItemMisc': ('Fighters', lambda cw: cw.fighters, exportFighters),
    'cargoItemMisc': ('Cargo Items', lambda cw: cw.cargo, exportCargo),
    'implantItemMisc': ('Implants', lambda cw: cw.implants, exportImplants),
    'implantItemMiscChar': ('Implants', lambda cw: cw.implants, exportImplants),
    'boosterItemMisc': ('Boosters', lambda cw: cw.boosters, exportBoosters)}


class AdditionsExportAll(ContextMenuUnconditional):

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
        if not viewSpecMap[srcContext][1](callingWindow):
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext):
        return 'Copy All {}'.format(viewSpecMap[self.srcContext][0])

    def activate(self, callingWindow, fullContext, i):
        items = viewSpecMap[self.srcContext][1](callingWindow)
        export = viewSpecMap[self.srcContext][2](items)
        if export:
            toClipboard(export)


AdditionsExportAll.register()
