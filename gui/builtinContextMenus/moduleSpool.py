import math

import wx

import eos.config
import gui.fitCommands as cmd
import gui.mainFrame
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from gui.contextMenu import ContextMenuSingle
from service.fit import Fit

# noinspection PyPackageRequirements

_t = wx.GetTranslation


class ChangeModuleSpool(ContextMenuSingle):
    visibilitySetting = 'spoolup'

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.resetId = None

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ('fittingModule', 'projectedModule') or self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None or mainItem.isEmpty:
            return False

        self.mod = mainItem
        self.context = srcContext

        return self.mod.item.group.name in ("Precursor Weapon", "Mutadaptive Remote Armor Repairer")

    def getText(self, callingWindow, itmContext, mainItem):
        return _t("Spoolup Cycles")

    def getSubMenu(self, callingWindow, context, mainItem, rootMenu, i, pitem):
        m = wx.Menu()
        if "wxMSW" in wx.PlatformInfo:
            bindmenu = rootMenu
        else:
            bindmenu = m

        isNotDefault = self.mod.spoolType is not None and self.mod.spoolAmount is not None
        cycleDefault = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, eos.config.settings['globalDefaultSpoolupPercentage'], True))[0]
        cycleCurrent = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, eos.config.settings['globalDefaultSpoolupPercentage'], False))[0]
        cycleMin = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 0, True))[0]
        cycleMax = self.mod.getSpoolData(spoolOptions=SpoolOptions(SpoolType.SPOOL_SCALE, 1, True))[0]
        cycleTotalMin = min(cycleDefault, cycleCurrent, cycleMin)
        cycleTotalMax = max(cycleDefault, cycleCurrent, cycleMax)

        def findCycles(val1, val2):
            # Try to compose list of 21 steps max (0-20)
            maxSteps = 20
            valDiff = val2 - val1
            valScale = valDiff / maxSteps
            minStep = math.ceil(round(valScale, 9))
            maxStep = math.floor(round(valDiff / 4, 9))
            # Check steps from smallest to highest and see if we can go from min value
            # to max value using those
            for currentStep in range(minStep, maxStep + 1):
                if valDiff % currentStep == 0:
                    return set(range(val1, val2 + currentStep, currentStep))
            # Otherwise just split range in halves and go both ends using min values
            else:
                cycles = set()
                while val2 >= val1:
                    cycles.add(val1)
                    cycles.add(val2)
                    val1 += minStep
                    val2 -= minStep
                return cycles

        self.cycleMap = {}
        cyclesToShow = findCycles(cycleMin, cycleMax)
        for cycle in range(cycleTotalMin, cycleTotalMax + 1):
            menuId = ContextMenuSingle.nextID()

            # Show default only for current value and when not overriden
            if not isNotDefault and cycle == cycleDefault:
                text = _t("{} (default)").format(cycle)
            # Always show current selection and stuff which we decided to show via the cycles function
            elif cycle == cycleCurrent or cycle in cyclesToShow:
                text = "{}".format(cycle)
            # Ignore the rest to not have very long menu
            else:
                continue

            item = wx.MenuItem(m, menuId, text, kind=wx.ITEM_CHECK)
            bindmenu.Bind(wx.EVT_MENU, self.handleSpoolChange, item)
            m.Append(item)
            item.Check(isNotDefault and cycle == cycleCurrent)
            self.cycleMap[menuId] = cycle

        self.resetId = ContextMenuSingle.nextID()
        item = wx.MenuItem(m, self.resetId, _t("Reset"))
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
