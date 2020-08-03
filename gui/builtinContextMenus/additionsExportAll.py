import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from gui.utils.clipboard import toClipboard
from service.fit import Fit
from service.port.eft import exportBoosters, exportCargo, exportDrones, exportFighters, exportImplants

_t = wx.GetTranslation


class AdditionsExportAll(ContextMenuUnconditional):
    visibilitySetting = 'additionsCopyPaste'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.viewSpecMap = {
            'droneItemMisc': (_t('Drones'), lambda cw: cw.drones, exportDrones),
            'fighterItemMisc': (_t('Fighters'), lambda cw: cw.fighters, exportFighters),
            'cargoItemMisc': (_t('Cargo Items'), lambda cw: cw.cargo, exportCargo),
            'implantItemMisc': (_t('Implants'), lambda cw: cw.implants, exportImplants),
            'implantItemMiscChar': (_t('Implants'), lambda cw: cw.implants, exportImplants),
            'boosterItemMisc': (_t('Boosters'), lambda cw: cw.boosters, exportBoosters)
        }

    def display(self, callingWindow, srcContext):
        if srcContext not in self.viewSpecMap:
            return False
        fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
        if fit is None:
            return False
        if not self.viewSpecMap[srcContext][1](callingWindow):
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext):
        return _t('Copy All {}').format(self.viewSpecMap[self.srcContext][0])

    def activate(self, callingWindow, fullContext, i):
        items = self.viewSpecMap[self.srcContext][1](callingWindow)
        export = self.viewSpecMap[self.srcContext][2](items)
        if export:
            toClipboard(export)


AdditionsExportAll.register()
