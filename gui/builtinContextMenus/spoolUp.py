# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from eos.utils.spoolSupport import SpoolType, SpoolOptions
from gui import globalEvents as GE
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings
from service.fit import Fit


class SpoolUp(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.cycleMap = {}
        self.resetId = None

    def display(self, srcContext, selection):
        if not self.settings.get('spoolup'):
            return False

        if srcContext not in ("fittingModule") or self.mainFrame.getActiveFit() is None:
            return False

        self.mod = selection[0]

        return self.mod.item.group.name in ("Precursor Weapon", "Mutadaptive Remote Armor Repairer")

    def getText(self, itmContext, selection):
        return "Spoolup"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        m = wx.Menu()
        cyclesMin = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SCALE, 0, True))[0]
        cyclesMax = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SCALE, 1, True))[0]

        for cycle in range(cyclesMin, cyclesMax + 1):
            menuId = ContextMenu.nextID()
            item = wx.MenuItem(m, menuId, "{}".format(cycle))
            m.Bind(wx.EVT_MENU, self.handleSpoolChange, item)
            m.Append(item)
            self.cycleMap[menuId] = cycle

        self.resetId = ContextMenu.nextID()
        item = wx.MenuItem(m, self.resetId, "Default")
        m.Bind(wx.EVT_MENU, self.handleSpoolChange, item)
        m.Append(item)

        return m

    def handleSpoolChange(self, event):
        if event.Id == self.resetId:
            self.mod.spoolType = None
            self.mod.spoolAmount = None
        elif event.Id in self.cycleMap:
            cycles = self.cycleMap[event.Id]
            self.mod.spoolType = SpoolType.CYCLES
            self.mod.spoolAmount = cycles
        fitID = self.mainFrame.getActiveFit()
        Fit.getInstance().recalc(fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


SpoolUp.register()
