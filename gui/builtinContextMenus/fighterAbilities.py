# noinspection PyPackageRequirements
import wx
from gui.contextMenu import ContextMenu
import gui.mainFrame
import gui.globalEvents as GE
from service.fit import Fit
from service.settings import ContextMenuSettings


class FighterAbility(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('fighterAbilities'):
            return False

        if self.mainFrame.getActiveFit() is None or srcContext not in ("fighterItem", "projectedFighter"):
            return False

        self.fighter = selection[0]
        return True

    def getText(self, itmContext, selection):
        return "Abilities"

    def addAbility(self, menu, ability):
        label = ability.name
        id = ContextMenu.nextID()
        self.abilityIds[id] = ability
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.context = context
        self.abilityIds = {}

        sub = wx.Menu()

        for ability in self.fighter.abilities:
            if not ability.effect.isImplemented:
                continue
            menuItem = self.addAbility(rootMenu if msw else sub, ability)
            sub.Append(menuItem)
            menuItem.Check(ability.active)

        return sub

    def handleMode(self, event):
        ability = self.abilityIds[event.Id]
        if ability is False or ability not in self.fighter.abilities:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.toggleFighterAbility(fitID, ability)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


FighterAbility.register()
