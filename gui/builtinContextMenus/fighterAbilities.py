# noinspection PyPackageRequirements

import wx

import gui.mainFrame
from gui import fitCommands as cmd
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import getSimilarFighters
from service.fit import Fit

_t = wx.GetTranslation


class FighterAbilities(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.isProjected = None

    def display(self, callingWindow, srcContext, mainItem, selection):
        if self.mainFrame.getActiveFit() is None or srcContext not in ("fighterItem", "projectedFighter"):
            return False

        if mainItem is None:
            return False

        self.fighter = mainItem
        self.selection = selection
        self.isProjected = True if srcContext == "projectedFighter" else False
        return True

    def getText(self, callingWindow, itmContext, mainItem, selection):
        return _t("Abilities")

    def addAbility(self, menu, ability):
        label = ability.name
        id = ContextMenuCombined.nextID()
        self.abilityIds[id] = ability
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, mainItem, selection, rootMenu, i, pitem):
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
            container = fit.projectedFighters
            command = cmd.GuiToggleProjectedFighterAbilityStateCommand
        else:
            container = fit.fighters
            command = cmd.GuiToggleLocalFighterAbilityStateCommand
        if self.fighter in container:
            mainPosition = container.index(self.fighter)
            if wx.GetMouseState().GetModifiers() in (wx.MOD_ALT, wx.MOD_CONTROL):
                fighters = getSimilarFighters(container, self.fighter)
            else:
                fighters = self.selection
            positions = []
            for fighter in fighters:
                if fighter in container:
                    positions.append(container.index(fighter))
            self.mainFrame.command.Submit(command(
                    fitID=fitID,
                    mainPosition=mainPosition,
                    positions=positions,
                    effectID=ability.effectID))


FighterAbilities.register()
