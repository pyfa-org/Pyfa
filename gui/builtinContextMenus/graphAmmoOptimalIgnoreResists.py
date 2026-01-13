# noinspection PyPackageRequirements

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import GraphSettings

_t = wx.GetTranslation


class GraphAmmoOptimalIgnoreResistsMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext == 'ammoOptimalDpsGraph'

    def getText(self, callingWindow, itmContext):
        return _t('Ignore Target Resists')

    def activate(self, callingWindow, fullContext, i):
        self.settings.set('ammoOptimalIgnoreResists', not self.settings.get('ammoOptimalIgnoreResists'))
        wx.PostEvent(self.mainFrame, GE.GraphOptionChanged(refreshAxeLabels=True, refreshColumns=True))

    def isChecked(self, i):
        return self.settings.get('ammoOptimalIgnoreResists')


GraphAmmoOptimalIgnoreResistsMenu.register()
