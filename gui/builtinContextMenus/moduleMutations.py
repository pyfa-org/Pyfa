# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands import GuiConvertMutatedLocalModuleCommand, GuiRevertMutatedLocalModuleCommand
from service.settings import ContextMenuSettings
from service.fit import Fit


class ChangeModuleMutation(ContextMenuCombined):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.eventIDs = {}

    def display(self, srcContext, mainItem, selection):
        if srcContext != "fittingModule" or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None or mainItem.isEmpty:
            return False

        if len(mainItem.item.mutaplasmids) == 0 and not mainItem.isMutated:
            return False

        return True

    def getText(self, itmContext, mainItem, selection):
        return "Apply Mutaplasmid" if not mainItem.isMutated else "Revert to {}".format(mainItem.baseItem.name)

    def getSubMenu(self, context, mainItem, selection, rootMenu, i, pitem):
        if mainItem.isMutated:
            return None

        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.skillIds = {}
        sub = wx.Menu()

        menu = rootMenu if msw else sub

        for item in mainItem.item.mutaplasmids:
            label = item.item.name
            id = ContextMenuCombined.nextID()
            self.eventIDs[id] = (item, mainItem)
            skillItem = wx.MenuItem(menu, id, label)
            menu.Bind(wx.EVT_MENU, self.handleMenu, skillItem)
            sub.Append(skillItem)

        return sub

    def handleMenu(self, event):
        mutaplasmid, mod = self.eventIDs[event.Id]
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mod in fit.modules:
            position = fit.modules.index(mod)
            self.mainFrame.command.Submit(GuiConvertMutatedLocalModuleCommand(
                fitID=fitID, position=position, mutaplasmid=mutaplasmid))

    def activate(self, fullContext, mainItem, selection, i):
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mainItem in fit.modules:
            position = fit.modules.index(mainItem)
            self.mainFrame.command.Submit(GuiRevertMutatedLocalModuleCommand(
                fitID=fitID, position=position))

    def getBitmap(self, context, mainItem, selection):
        return None


ChangeModuleMutation.register()
