# noinspection PyPackageRequirements

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import GraphSettings

_t = wx.GetTranslation


class GraphIgnoreLockRangeMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext in ('dmgStatsGraph', 'remoteRepsGraph', 'ewarStatsGraph')

    def getText(self, callingWindow, itmContext):
        return _t('Ignore Lock Range')

    def activate(self, callingWindow, fullContext, i):
        self.settings.set('ignoreLockRange', not self.settings.get('ignoreLockRange'))
        wx.PostEvent(self.mainFrame, GE.GraphOptionChanged())

    def isChecked(self, i):
        return self.settings.get('ignoreLockRange')


GraphIgnoreLockRangeMenu.register()
