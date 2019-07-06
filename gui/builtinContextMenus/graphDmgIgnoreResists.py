# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import GraphSettings


class GraphDmgIgnoreResists(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, srcContext):
        return srcContext == 'dmgStatsGraph'

    def getText(self, itmContext):
        return "Ignore Target Resists"

    def activate(self, fullContext, i):
        self.settings.set('ignoreResists', not self.settings.get('ignoreResists'))
        wx.PostEvent(self.mainFrame, GE.GraphOptionChanged())

    @property
    def checked(self):
        return self.settings.get('ignoreResists')


GraphDmgIgnoreResists.register()
