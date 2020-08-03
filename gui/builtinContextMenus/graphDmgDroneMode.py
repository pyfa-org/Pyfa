from collections import OrderedDict

import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.const import GraphDpsDroneMode
from service.settings import GraphSettings

# noinspection PyPackageRequirements

_t = wx.GetTranslation


class GraphDmgDroneModeMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, callingWindow, srcContext):
        return srcContext == 'dmgStatsGraph'

    def getText(self, callingWindow, itmContext):
        return _t('Drone Mode')

    def handleModeSwitch(self, event):
        option = self.idOptionMap[event.Id]
        if option == self.settings.get('mobileDroneMode'):
            return
        self.settings.set('mobileDroneMode', option)
        wx.PostEvent(self.mainFrame, GE.GraphOptionChanged())

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        m = wx.Menu()
        if "wxMSW" in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m
        self.idOptionMap = {}
        optionMap = OrderedDict([
            (GraphDpsDroneMode.auto, _t('Auto')),
            (GraphDpsDroneMode.followTarget, _t('Stick to Target')),
            (GraphDpsDroneMode.followAttacker, _t('Stick to Attacker'))])
        for option, label in optionMap.items():
            menuId = ContextMenuUnconditional.nextID()
            item = wx.MenuItem(m, menuId, label, kind=wx.ITEM_CHECK)
            bindmenu.Bind(wx.EVT_MENU, self.handleModeSwitch, item)
            m.Append(item)
            item.Check(option == self.settings.get('mobileDroneMode'))
            self.idOptionMap[menuId] = option
        return m


GraphDmgDroneModeMenu.register()
