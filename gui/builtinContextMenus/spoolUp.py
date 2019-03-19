# noinspection PyPackageRequirements
import wx

import eos.config
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
        return "Spoolup Cycles"

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        m = wx.Menu()
        if "wxMSW" in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m

        isNotDefault = self.mod.spoolType is not None and self.mod.spoolAmount is not None
        cycleDefault = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SCALE, eos.config.settings['globalDefaultSpoolupPercentage'], True))[0]
        cycleCurrent = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SCALE, eos.config.settings['globalDefaultSpoolupPercentage'], False))[0]
        cycleMin = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SCALE, 0, True))[0]
        cycleMax = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SCALE, 1, True))[0]

        for cycle in range(cycleMin, cycleMax + 1):
            menuId = ContextMenu.nextID()

            # Show default only for current value and when not overriden
            if not isNotDefault and cycle == cycleDefault:
                text = "{} (default)".format(cycle)
            else:
                text = "{}".format(cycle)

            item = wx.MenuItem(m, menuId, text, kind=wx.ITEM_CHECK)
            bindmenu.Bind(wx.EVT_MENU, self.handleSpoolChange, item)
            m.Append(item)
            item.Check(isNotDefault and cycle == cycleCurrent)
            self.cycleMap[menuId] = cycle

        self.resetId = ContextMenu.nextID()
        item = wx.MenuItem(m, self.resetId, "Reset")
        bindmenu.Bind(wx.EVT_MENU, self.handleSpoolChange, item)
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
