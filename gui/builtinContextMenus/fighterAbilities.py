import wx
from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.globalEvents as GE

class FighterAbility(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        if self.mainFrame.getActiveFit() is None or srcContext != "fighterItem":
            return False

        self.fighter = selection[0]
        return True

    def getText(self, itmContext, selection):
        return "Abilities"

    def addAbility(self, menu, ability):
        label = ability.name
        id = wx.NewId()
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
            menuItem = self.addAbility(rootMenu if msw else sub, ability)
            sub.AppendItem(menuItem)
            menuItem.Check(ability.active)

        return sub

    def handleMode(self, event):
        ability = self.abilityIds[event.Id]
        if ability is False or ability not in self.fighter.abilities:
            event.Skip()
            return

        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        sFit.toggleFighterAbility(fitID, ability)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

FighterAbility.register()
