import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSelection
from gui.utils.clipboard import toClipboard
from service.fit import Fit
from service.port.eft import exportBoosters, exportCargo, exportDrones, exportFighters, exportImplants

_t = wx.GetTranslation


class AdditionsExportAll(ContextMenuSelection):
    visibilitySetting = 'additionsCopyPaste'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.viewSpecMap = {
            'droneItemMisc': (_t('Drones'), exportDrones),
            'fighterItemMisc': (_t('Fighters'), exportFighters),
            'cargoItemMisc': (_t('Cargo Items'), exportCargo),
            'implantItemMisc': (_t('Implants'), exportImplants),
            'implantItemMiscChar': (_t('Implants'), exportImplants),
            'boosterItemMisc': (_t('Boosters'), exportBoosters)
        }

    def display(self, callingWindow, srcContext, selection):
        if srcContext not in self.viewSpecMap:
            return False
        if not selection:
            return False
        fit = Fit.getInstance().getFit(self.mainFrame.getActiveFit())
        if fit is None:
            return False

        self.srcContext = srcContext
        return True

    def getText(self, callingWindow, itmContext, selection):
        return _t('Copy Selected {}').format(self.viewSpecMap[self.srcContext][0])

    def activate(self, callingWindow, fullContext, selection, i):
        export = self.viewSpecMap[self.srcContext][1](selection)
        if export:
            toClipboard(export)


AdditionsExportAll.register()
