# noinspection PyPackageRequirements

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import GraphSettings

_t = wx.GetTranslation


class GraphIgnoreDcrMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext in ('dmgStatsGraph', 'remoteRepsGraph', 'ewarStatsGraph')

    def getText(self, callingWindow, itmContext):
        return _t('Ignore Drone Control Range')

    def activate(self, callingWindow, fullContext, i):
        self.settings.set('ignoreDCR', not self.settings.get('ignoreDCR'))
        wx.PostEvent(self.mainFrame, GE.GraphOptionChanged())

    def isChecked(self, i):
        return self.settings.get('ignoreDCR')


GraphIgnoreDcrMenu.register()
