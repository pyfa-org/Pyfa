# noinspection PyPackageRequirements

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import GraphSettings

_t = wx.GetTranslation


class GraphAmmoOptimalApplyProjectedMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext == 'ammoOptimalDpsGraph'

    def getText(self, callingWindow, itmContext):
        return _t('Apply Projected Effects')

    def activate(self, callingWindow, fullContext, i):
        self.settings.set('ammoOptimalApplyProjected', not self.settings.get('ammoOptimalApplyProjected'))
        wx.PostEvent(self.mainFrame, GE.GraphOptionChanged())

    def isChecked(self, i):
        return self.settings.get('ammoOptimalApplyProjected')


GraphAmmoOptimalApplyProjectedMenu.register()
