# noinspection PyPackageRequirements
import wx

import gui.globalEvents as GE
import gui.mainFrame
from gui.fitCommands import GuiMutaConvertCommand
from gui.contextMenu import ContextMenu
from service.fit import Fit
from service.settings import ContextMenuSettings


class MutaplasmidCM(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.eventIDs = {}

    def display(self, srcContext, selection):

        # if not self.settings.get('ammoPattern'):
        #     return False

        if srcContext not in "fittingModule" or self.mainFrame.getActiveFit() is None:
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

        self.mainFrame.command.Submit(GuiMutaConvertCommand(
            fitID=self.mainFrame.getActiveFit(),
            position=mod.modPosition,
            mutaplasmid=mutaplasmid))

    def activate(self, fullContext, selection, i):
        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        mod = selection[0]
        sFit.changeModule(fitID, mod.modPosition, mod.baseItemID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

    def getBitmap(self, context, selection):
        return None


MutaplasmidCM.register()
