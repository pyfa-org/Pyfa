# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui import fitCommands as cmd
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class BoosterSideEffect(ContextMenu):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, mainItem, selection):
        if self.mainFrame.getActiveFit() is None or srcContext not in "boosterItem":
            return False

        if mainItem is None:
            return False

        self.booster = mainItem

        for effect in self.booster.sideEffects:
            if effect.effect.isImplemented:
                return True

        return False

    def getText(self, itmContext, mainItem, selection):
        return "Side Effects"

    def addEffect(self, menu, ability):
        label = ability.name
        id = ContextMenu.nextID()
        self.effectIds[id] = ability

        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, context, mainItem, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.context = context
        self.effectIds = {}

        sub = wx.Menu()

        for effect in self.booster.sideEffects:
            if not effect.effect.isImplemented:
                continue
            menuItem = self.addEffect(rootMenu if msw else sub, effect)
            sub.Append(menuItem)
            menuItem.Check(effect.active)

        return sub

    def handleMode(self, event):
        effect = self.effectIds[event.Id]
        booster = self.booster
        if effect is False or effect not in booster.sideEffects:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if booster in fit.boosters:
            index = fit.boosters.index(booster)
            self.mainFrame.command.Submit(cmd.GuiToggleBoosterSideEffectStateCommand(
                fitID=fitID, position=index, effectID=effect.effectID))


BoosterSideEffect.register()
