import wx

import eos.db
import gui.mainFrame
from eos.const import FittingModuleState
from eos.saveddata.drone import Drone as EosDrone
from eos.saveddata.fighter import Fighter as EosFighter
from eos.saveddata.fit import Fit as EosFit
from eos.saveddata.module import Module as EosModule
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.projectedChangeState import CalcChangeProjectedDroneStateCommand
from gui.fitCommands.calc.fighter.projectedChangeState import CalcChangeProjectedFighterStateCommand
from gui.fitCommands.calc.module.projectedChangeStates import CalcChangeProjectedModuleStatesCommand
from gui.fitCommands.calc.projectedFit.changeState import CalcChangeProjectedFitStateCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedItemStatesCommand(wx.Command):

    def __init__(self, fitID, mainItem, items, click):
        wx.Command.__init__(self, True, 'Change Projected Item States')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.pModPositions = []
        self.pDroneItemIDs = []
        self.pFighterPositions = []
        self.pFitIDs = []
        fit = Fit.getInstance().getFit(fitID)
        for item in items:
            if isinstance(item, EosModule):
                if item in fit.projectedModules:
                    self.pModPositions.append(fit.projectedModules.index(item))
            elif isinstance(item, EosDrone):
                self.pDroneItemIDs.append(item.itemID)
            elif isinstance(item, EosFighter):
                if item in fit.projectedFighters:
                    self.pFighterPositions.append(fit.projectedFighters.index(item))
            elif isinstance(item, EosFit):
                self.pFitIDs.append(item.ID)
        self.proposedState = None
        if click == 'right' and isinstance(mainItem, EosModule):
            self.proposedState = 'overheat'
        elif click == 'left':
            if isinstance(mainItem, EosModule):
                modProposedState = EosModule.getProposedState(mainItem, click)
                self.proposedState = 'inactive' if modProposedState == FittingModuleState.OFFLINE else 'active'
            elif isinstance(mainItem, EosDrone):
                self.proposedState = 'active' if mainItem.amountActive == 0 else 'inactive'
            elif isinstance(mainItem, EosFighter):
                self.proposedState = 'inactive' if mainItem.active else 'active'
            elif isinstance(mainItem, EosFit):
                projectionInfo = mainItem.getProjectionInfo(self.fitID)
                if projectionInfo is not None:
                    self.proposedState = 'inactive' if projectionInfo.active else 'active'

    def Do(self):
        if self.proposedState is None:
            return False
        results = []
        needRecalc = True
        if self.pModPositions:
            cmd = CalcChangeProjectedModuleStatesCommand(
                fitID=self.fitID,
                positions=self.pModPositions,
                proposedState=self.proposedState)
            results.append(self.internalHistory.submit(cmd))
            needRecalc = cmd.needsGuiRecalc
        for pDroneItemID in self.pDroneItemIDs:
            cmd = CalcChangeProjectedDroneStateCommand(
                fitID=self.fitID,
                itemID=pDroneItemID,
                state=False if self.proposedState == 'inactive' else True)
            results.append(self.internalHistory.submit(cmd))
            needRecalc = True
        for pFighterPosition in self.pFighterPositions:
            cmd = CalcChangeProjectedFighterStateCommand(
                fitID=self.fitID,
                position=pFighterPosition,
                state=False if self.proposedState == 'inactive' else True)
            results.append(self.internalHistory.submit(cmd))
            needRecalc = True
        for pFitID in self.pFitIDs:
            cmd = CalcChangeProjectedFitStateCommand(
                fitID=self.fitID,
                projectedFitID=pFitID,
                state=False if self.proposedState == 'inactive' else True)
            results.append(self.internalHistory.submit(cmd))
            needRecalc = cmd.needsGuiRecalc
        success = any(results)
        sFit = Fit.getInstance()
        if needRecalc:
            eos.db.flush()
            sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
