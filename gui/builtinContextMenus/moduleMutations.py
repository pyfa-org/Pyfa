# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenu
from gui.fitCommands import GuiConvertMutatedLocalModuleCommand, GuiRevertMutatedLocalModuleCommand
from service.settings import ContextMenuSettings
from service.fit import Fit


class ChangeModuleMutation(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.eventIDs = {}

    def display(self, srcContext, mainItem, selection):

        # if not self.settings.get('ammoPattern'):
        #     return False

        if srcContext != "fittingModule" or self.mainFrame.getActiveFit() is None:
            return False

        mod = selection[0]
        if len(mod.item.mutaplasmids) == 0 and not mod.isMutated:
            return False

        return True

    def getText(self, itmContext, mainItem, selection):
        mod = selection[0]
        return "Apply Mutaplasmid" if not mod.isMutated else "Revert to {}".format(mod.baseItem.name)

    def getSubMenu(self, context, mainItem, selection, rootMenu, i, pitem):
        if selection[0].isMutated:
            return None

        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.skillIds = {}
        sub = wx.Menu()

        mod = selection[0]

        menu = rootMenu if msw else sub

        for item in mod.item.mutaplasmids:
            label = item.item.name
            id = ContextMenu.nextID()
            self.eventIDs[id] = (item, mod)
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
        mod = selection[0]
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if mod in fit.modules:
            position = fit.modules.index(mod)
            self.mainFrame.command.Submit(GuiRevertMutatedLocalModuleCommand(
                fitID=fitID, position=position))

    def getBitmap(self, context, mainItem, selection):
        return None


ChangeModuleMutation.register()
