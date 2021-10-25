import re

# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from gui.fitCommands import (
    GuiConvertMutatedLocalModuleCommand, GuiRevertMutatedLocalModuleCommand,
    GuiConvertMutatedLocalDroneCommand, GuiRevertMutatedLocalDroneCommand)
from service.fit import Fit

_t = wx.GetTranslation


class ChangeItemMutation(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.eventIDs = {}

    def display(self, callingWindow, srcContext, mainItem):

        if srcContext not in ("fittingModule", "droneItem") or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None or getattr(mainItem, 'isEmpty', False):
            return False

        if len(mainItem.item.mutaplasmids) == 0 and not mainItem.isMutated:
            return False

        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Apply Mutaplasmid") if not mainItem.isMutated else _t("Revert to {}").format(mainItem.baseItem.name)

    def getSubMenu(self, callingWindow, context, mainItem, rootMenu, i, pitem):
        if mainItem.isMutated:
            return None

        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.skillIds = {}
        sub = wx.Menu()

        menu = rootMenu if msw else sub

        for mutaplasmid in mainItem.item.mutaplasmids:
            id = ContextMenuSingle.nextID()
            self.eventIDs[id] = (mutaplasmid, mainItem)
            mItem = wx.MenuItem(menu, id, mutaplasmid.shortName)
            menu.Bind(wx.EVT_MENU, self.handleMenu, mItem)
            sub.Append(mItem)

        return sub

    def handleMenu(self, event):
        mutaplasmid, item = self.eventIDs[event.Id]
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if item in fit.modules:
            position = fit.modules.index(item)
            self.mainFrame.command.Submit(GuiConvertMutatedLocalModuleCommand(
                    fitID=fitID, position=position, mutaplasmid=mutaplasmid))
        elif item in fit.drones:
            position = fit.drones.index(item)
            self.mainFrame.command.Submit(GuiConvertMutatedLocalDroneCommand(
                    fitID=fitID, position=position, mutaplasmid=mutaplasmid))

    def activate(self, callingWindow, fullContext, mainItem, i):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mainItem in fit.modules:
            position = fit.modules.index(mainItem)
            self.mainFrame.command.Submit(GuiRevertMutatedLocalModuleCommand(
                    fitID=fitID, position=position))
        elif mainItem in fit.drones:
            position = fit.drones.index(mainItem)
            self.mainFrame.command.Submit(GuiRevertMutatedLocalDroneCommand(
                    fitID=fitID, position=position))

    def getBitmap(self, callingWindow, context, mainItem):
        return None


ChangeItemMutation.register()
