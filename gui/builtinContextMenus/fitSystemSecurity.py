from collections import OrderedDict

import wx

import gui.fitCommands as cmd
import gui.mainFrame
from eos.const import FitSystemSecurity
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit


optionMap = OrderedDict((
    ('High Security', FitSystemSecurity.HISEC),
    ('Low Security', FitSystemSecurity.LOWSEC),
    ('Null Security', FitSystemSecurity.NULLSEC),
    ('W-Space', FitSystemSecurity.WSPACE)))


class FitSystemSecurityMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext):
        if srcContext != "fittingShip":
            return False

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        if not fit.isStructure:
            return

        return True

    def getText(self, itmContext):
        return "Citadel System Security"

    def addOption(self, menu, optionLabel):
        id = ContextMenuUnconditional.nextID()
        self.optionIds[id] = optionLabel
        menuItem = wx.MenuItem(menu, id, optionLabel, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, context, rootMenu, i, pitem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.optionIds = {}
        sub = wx.Menu()
        for optionLabel, optionValue in optionMap.items():
            menuItem = self.addOption(rootMenu if msw else sub, optionLabel)
            sub.Append(menuItem)
            menuItem.Check(fit.getSystemSecurity() == optionValue)

        return sub

    def handleMode(self, event):
        optionLabel = self.optionIds[event.Id]
        optionValue = optionMap[optionLabel]
        self.mainFrame.command.Submit(cmd.GuiChangeFitSystemSecurityCommand(
            fitID=self.mainFrame.getActiveFit(),
            secStatus=optionValue))


FitSystemSecurityMenu.register()
