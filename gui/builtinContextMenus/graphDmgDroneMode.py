from collections import OrderedDict

# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.settings import GraphSettings


class TargetResists(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = GraphSettings.getInstance()

    def display(self, srcContext):
        return srcContext == 'dmgStatsGraph'

    def getText(self, itmContext):
        return 'Drone Mode'

    def handleModeSwitch(self, event):
        optionName = self.idOptionMap[event.Id]
        self.settings.set('mobileDroneMode', optionName)

    def getSubMenu(self, context, rootMenu, i, pitem):
        m = wx.Menu()
        if "wxMSW" in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m
        self.idOptionMap = {}
        optionMap = OrderedDict([('auto', 'Auto'), ('followSelf', 'Stick to attacker'), ('followTgt', 'Stick to target')])
        for optionName, label in optionMap.items():
            menuId = ContextMenuUnconditional.nextID()
            item = wx.MenuItem(m, menuId, label, kind=wx.ITEM_CHECK)
            bindmenu.Bind(wx.EVT_MENU, self.handleModeSwitch, item)
            m.Append(item)
            item.Check(optionName == self.settings.get('mobileDroneMode'))
            self.idOptionMap[menuId] = optionName
        return m


TargetResists.register()
