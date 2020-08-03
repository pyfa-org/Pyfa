# noinspection PyPackageRequirements

import wx

import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuUnconditional
from service.fit import Fit

_t = wx.GetTranslation


class ChangeShipTacticalMode(ContextMenuUnconditional):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.modeMap = {
            'Defense': _t('Defense'),
            'Propulsion': _t('Propulsion'),
            'Sharpshooter': _t('Sharpshooter')
        }

    def display(self, callingWindow, srcContext):
        if self.mainFrame.getActiveFit() is None or srcContext != "fittingShip":
            return False

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        fit = sFit.getFit(fitID)

        self.modes = fit.ship.modes
        self.currMode = fit.mode

        return srcContext == "fittingShip" and self.modes is not None

    def getText(self, callingWindow, itmContext):
        return _t("Tactical Mode")

    def addMode(self, menu, mode):
        key = mode.item.typeName.rsplit()[-2]
        label = self.modeMap[key]

        id = ContextMenuUnconditional.nextID()
        self.modeIds[id] = mode
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_RADIO)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, callingWindow, context, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.context = context
        self.modeIds = {}

        sub = wx.Menu()

        for mode in self.modes:
            menuItem = self.addMode(rootMenu if msw else sub, mode)
            sub.Append(menuItem)
            menuItem.Check(self.currMode.item == mode.item)

        return sub

    def handleMode(self, event):
        item = self.modeIds[event.Id]
        if item is False or item not in self.modes:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        self.mainFrame.command.Submit(cmd.GuiChangeShipModeCommand(fitID, self.modeIds[event.Id].item.ID))


ChangeShipTacticalMode.register()
