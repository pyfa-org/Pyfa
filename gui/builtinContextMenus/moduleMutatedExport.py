import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from gui.utils.clipboard import toClipboard
from service.port.muta import renderMutant

_t = wx.GetTranslation


class ExportMutatedModule(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext != 'fittingModule':
            return False
        if self.mainFrame.getActiveFit() is None:
            return False
        if mainItem is None:
            return False
        if not mainItem.isMutated:
            return False
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return _t('Copy Module to Clipboard')

    def activate(self, callingWindow, fullContext, mainItem, i):
        export = renderMutant(mainItem, prefix='  ')
        toClipboard(export)


ExportMutatedModule.register()
