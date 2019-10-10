# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSingle


class GraphFitAmmoPicker(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext != 'graphFitList':
            return False
        if mainItem is None or not mainItem.isFit:
            return False
        if callingWindow.graphFrame.getView().internalName != 'dmgStatsGraph':
            return False
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return 'Plot with Different Ammo...'

    def activate(self, callingWindow, fullContext, mainItem, i):
        with AmmoPicker(self.mainFrame) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                pass
            else:
                pass


GraphFitAmmoPicker.register()


class AmmoPicker(wx.Dialog):

    def __init__(self, parent):
        super().__init__(parent, title='Choose Different Ammo', style=wx.DEFAULT_DIALOG_STYLE)
        self.SetMinSize((346, 156))
