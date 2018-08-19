import wx

import gui.mainFrame
from gui.contextMenu import ContextMenu
from service.settings import InsuranceMenuSettings


class InsuranceOptions(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = InsuranceMenuSettings.getInstance()
        self.optionList = ["Cost", "Payout", "Difference"]

    def display(self, srcContext, selection):
        return srcContext in ("insuranceViewFull")

    def getText(self, itmContext, selection):
        return "Column Display (Requires Restart)"

    def addOption(self, menu, option):
        label = option
        id = ContextMenu.nextID()
        self.optionIds[id] = option
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.context = context
        self.optionIds = {}

        sub = wx.Menu()

        for option in self.optionList:
            menuItem = self.addOption(rootMenu if msw else sub, option)
            sub.Append(menuItem)
            menuItem.Check(self.settings.get(option.lower()))

        return sub

    def handleMode(self, event):
        option = self.optionIds[event.Id]
        self.settings.set(option.lower(), event.Int)


InsuranceOptions.register()
