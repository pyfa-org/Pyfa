import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo, restoreRemovedDummies
from service.fit import Fit


class GuiChangeLocalModuleMetasCommand(wx.Command):

    def __init__(self, fitID, positions, newItemID):
        wx.Command.__init__(self, True, 'Change Local Module Metas')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.positions = positions
        self.newItemID = newItemID
        self.replacedItemIDs = None
        self.savedRemovedDummies = None

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldModMap = self._getPositionMap(fit)
        results = []
        self.replacedItemIDs = set()
        lastSuccessfulCmd = None
        for position in self.positions:
            module = fit.modules[position]
            if module.isEmpty:
                continue
            if module.itemID == self.newItemID:
                continue
            info = ModuleInfo.fromModule(module)
            info.itemID = self.newItemID
            cmd = CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=position,
                newModInfo=info,
                unloadInvalidCharges=True)
            result = self.internalHistory.submit(cmd)
            results.append(result)
            if result:
                self.replacedItemIDs.add(module.itemID)
                lastSuccessfulCmd = cmd
        success = any(results)
        if lastSuccessfulCmd is not None and lastSuccessfulCmd.needsGuiRecalc:
            eos.db.flush()
            sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        eos.db.commit()
        newModMap = self._getPositionMap(fit)
        events = []
        if success and self.replacedItemIDs:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.replacedItemIDs))
        if success:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.newItemID))
        if not events:
            events.append(GE.FitChanged(fitIDs=(self.fitID,)))
        if success:
            for position in self.positions:
                oldMod = oldModMap.get(position)
                newMod = newModMap.get(position)
                if oldMod is not newMod:
                    events.append(GE.ItemChangedInplace(old=oldMod, new=newMod))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        oldModMap = self._getPositionMap(fit)
        for position in self.positions:
            oldModMap[position] = fit.modules[position]
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        newModMap = self._getPositionMap(fit)
        events = []
        if success:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.newItemID))
        if success and self.replacedItemIDs:
            events.append(GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.replacedItemIDs))
        if not events:
            events.append(GE.FitChanged(fitIDs=(self.fitID,)))
        if success:
            for position in self.positions:
                oldMod = oldModMap.get(position)
                newMod = newModMap.get(position)
                if oldMod is not newMod:
                    events.append(GE.ItemChangedInplace(fitID=self.fitID, old=oldMod, new=newMod))
        for event in events:
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success

    def _getPositionMap(self, fit):
        positionMap = {}
        for position in self.positions:
            positionMap[position] = fit.modules[position]
        return positionMap
