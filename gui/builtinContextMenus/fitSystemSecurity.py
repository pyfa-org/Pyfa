from collections import OrderedDict

import wx

import gui.fitCommands as cmd
import gui.mainFrame
from eos.const import FitSystemSecurity
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit

_t = wx.GetTranslation


class FitSystemSecurityMenu(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.optionMap = OrderedDict((
            (_t('High Security'), FitSystemSecurity.HISEC),
            (_t('Low Security'), FitSystemSecurity.LOWSEC),
            (_t('Null Security'), FitSystemSecurity.NULLSEC),
            (_t('W-Space'), FitSystemSecurity.WSPACE)))

    def display(self, callingWindow, srcContext):
        if srcContext != "fittingShip":
            return False

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)

        if not fit.isStructure:
            return

        return True

    def getText(self, callingWindow, itmContext):
        return _t("Citadel System Security")

    def addOption(self, menu, optionLabel):
        id = ContextMenuUnconditional.nextID()
        self.optionIds[id] = optionLabel
        menuItem = wx.MenuItem(menu, id, optionLabel, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.optionIds = {}
        sub = wx.Menu()
        for optionLabel, optionValue in self.optionMap.items():
            menuItem = self.addOption(rootMenu if msw else sub, optionLabel)
            sub.Append(menuItem)
            menuItem.Check(fit.getSystemSecurity() == optionValue)

        return sub

    def handleMode(self, event):
        optionLabel = self.optionIds[event.Id]
        optionValue = self.optionMap[optionLabel]
        self.mainFrame.command.Submit(cmd.GuiChangeFitSystemSecurityCommand(
                fitID=self.mainFrame.getActiveFit(),
                secStatus=optionValue))


FitSystemSecurityMenu.register()
