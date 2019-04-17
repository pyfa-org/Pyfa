# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenu
from gui.fitCommands import GuiConvertMutatedLocalModuleCommand, GuiRevertMutatedLocalModuleCommand
from service.settings import ContextMenuSettings


class ChangeModuleMutation(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.eventIDs = {}

    def display(self, srcContext, selection):

        # if not self.settings.get('ammoPattern'):
        #     return False

        if srcContext != "fittingModule" or self.mainFrame.getActiveFit() is None:
            return False

        mod = selection[0]
        if len(mod.item.mutaplasmids) == 0 and not mod.isMutated:
            return False

        return True

    def getText(self, itmContext, selection):
        mod = selection[0]
        return "Apply Mutaplasmid" if not mod.isMutated else "Revert to {}".format(mod.baseItem.name)

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
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

        self.mainFrame.command.Submit(GuiConvertMutatedLocalModuleCommand(
            fitID=self.mainFrame.getActiveFit(),
            position=mod.modPosition,
            mutaplasmid=mutaplasmid))

    def activate(self, fullContext, selection, i):
        mod = selection[0]
        self.mainFrame.command.Submit(GuiRevertMutatedLocalModuleCommand(
            fitID=self.mainFrame.getActiveFit(),
            position=mod.modPosition))

    def getBitmap(self, context, selection):
        return None


ChangeModuleMutation.register()
