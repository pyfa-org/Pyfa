# noinspection PyPackageRequirements
import wx

import eos.config
import gui.fitCommands as cmd
import gui.mainFrame
from eos.utils.spoolSupport import SpoolType, SpoolOptions
from gui.contextMenu import ContextMenu
from service.settings import ContextMenuSettings
from service.fit import Fit


class ChangeModuleSpool(ContextMenu):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        self.cycleMap = {}
        self.resetId = None

    def display(self, srcContext, mainItem, selection):
        if not self.settings.get('spoolup'):
            return False

        if srcContext not in ('fittingModule', 'projectedModule') or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None or mainItem.isEmpty:
            return False

        self.mod = mainItem
        self.context = srcContext

        return self.mod.item.group.name in ("Precursor Weapon", "Mutadaptive Remote Armor Repairer")

    def getText(self, itmContext, mainItem, selection):
        return "Spoolup Cycles"

    def getSubMenu(self, context, mainItem, selection, rootMenu, i, pitem):
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
            spoolType = None
            spoolAmount = None
        elif event.Id in self.cycleMap:
            spoolType = SpoolType.CYCLES
            spoolAmount = self.cycleMap[event.Id]
        else:
            return
        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        if self.context == 'fittingModule':
            if self.mod in fit.modules:
                position = fit.modules.index(self.mod)
                self.mainFrame.command.Submit(cmd.GuiChangeLocalModuleSpoolCommand(
                    fitID=fitID, position=position, spoolType=spoolType, spoolAmount=spoolAmount))
        elif self.context == 'projectedModule':
            if self.mod in fit.projectedModules:
                position = fit.projectedModules.index(self.mod)
                self.mainFrame.command.Submit(cmd.GuiChangeProjectedModuleSpoolCommand(
                    fitID=fitID, position=position, spoolType=spoolType, spoolAmount=spoolAmount))


ChangeModuleSpool.register()
