# noinspection PyPackageRequirements

import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional

_t = wx.GetTranslation


class AddBrowsedFits(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext):
        if srcContext not in ('projected', 'commandView', 'graphFitList', 'graphTgtList'):
            return False
        return True

    def getText(self, callingWindow, itmContext):
        return _t('Add Fit...')

    def activate(self, callingWindow, fullContext, i):
        from gui.fitBrowserLite import FitBrowserLiteDialog
        titles = {
            'projected': 'Add Projected Fits',
            'commandView': 'Add Command Fits',
            'graphFitList': 'Add Fits to Graph',
            'graphTgtList': 'Add Targets to Graph'
        }
        excludedFitIDs = callingWindow.getExistingFitIDs()
        with FitBrowserLiteDialog(self.mainFrame, title=titles[fullContext[0]], excludedFitIDs=excludedFitIDs) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                fitIDs = dlg.getFitIDsToAdd()
                callingWindow.addFitsByIDs(fitIDs)


AddBrowsedFits.register()
