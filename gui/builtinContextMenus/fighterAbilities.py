# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui import fitCommands as cmd
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class FighterAbility(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.isProjected = None

    def display(self, srcContext, selection):
        if not self.settings.get('fighterAbilities'):
            return False

        if self.mainFrame.getActiveFit() is None or srcContext not in ("fighterItem", "projectedFighter"):
            return False

        self.fighter = selection[0]
        self.isProjected = True if srcContext == "projectedFighter" else False
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

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if self.isProjected:
            self.mainFrame.command.Submit(cmd.GuiToggleProjectedFighterAbilityStateCommand(
                fitID=fitID, position=fit.projectedFighters.index(self.fighter), effectID=ability.effectID))
        else:
            self.mainFrame.command.Submit(cmd.GuiToggleLocalFighterAbilityStateCommand(
                fitID=fitID, position=fit.fighters.index(self.fighter), effectID=ability.effectID))



FighterAbility.register()
