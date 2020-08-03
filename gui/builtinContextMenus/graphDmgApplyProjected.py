# noinspection PyPackageRequirements

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import GraphSettings

_t = wx.GetTranslation


class GraphDmgApplyProjectedMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext == 'dmgStatsGraph'

    def getText(self, callingWindow, itmContext):
        return _t('Apply Projected Items')

    def activate(self, callingWindow, fullContext, i):
        self.settings.set('applyProjected', not self.settings.get('applyProjected'))
        wx.PostEvent(self.mainFrame, GE.GraphOptionChanged())

    def isChecked(self, i):
        return self.settings.get('applyProjected')


GraphDmgApplyProjectedMenu.register()
