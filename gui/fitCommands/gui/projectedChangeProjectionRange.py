import wx

import eos.db
import gui.mainFrame
from eos.saveddata.drone import Drone as EosDrone
from eos.saveddata.fighter import Fighter as EosFighter
from eos.saveddata.fit import Fit as EosFit
from eos.saveddata.module import Module as EosModule
from gui import globalEvents as GE
from gui.fitCommands.calc.drone.projectedChangeProjectionRange import CalcChangeProjectedDroneProjectionRangeCommand
from gui.fitCommands.calc.fighter.projectedChangeProjectionRange import CalcChangeProjectedFighterProjectionRangeCommand
from gui.fitCommands.calc.module.projectedChangeProjectionRange import CalcChangeProjectedModuleProjectionRangeCommand
from gui.fitCommands.calc.projectedFit.changeProjectionRange import CalcChangeProjectedFitProjectionRangeCommand
from gui.fitCommands.helpers import InternalCommandHistory
from service.fit import Fit


class GuiChangeProjectedItemsProjectionRangeCommand(wx.Command):

    def __init__(self, fitID, items, projectionRange):
        wx.Command.__init__(self, True, 'Change Projected Items Projection Range')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.projectionRange = projectionRange
        self.pModPositions = []
        self.pDroneItemIDs = []
        self.pFighterPositions = []
        self.pFitIDs = []
        fit = Fit.getInstance().getFit(fitID)
        for item in items:
            if isinstance(item, EosModule):
                if item in fit.projectedModules and not getattr(item, 'isExclusiveSystemEffect', False):
                    self.pModPositions.append(fit.projectedModules.index(item))
            elif isinstance(item, EosDrone):
                self.pDroneItemIDs.append(item.itemID)
            elif isinstance(item, EosFighter):
                if item in fit.projectedFighters:
                    self.pFighterPositions.append(fit.projectedFighters.index(item))
            elif isinstance(item, EosFit):
                self.pFitIDs.append(item.ID)

    def Do(self):
        results = []
        needRecalc = True
        for pModPosition in self.pModPositions:
            cmd = CalcChangeProjectedModuleProjectionRangeCommand(
                fitID=self.fitID,
                position=pModPosition,
                projectionRange=self.projectionRange)
            results.append(self.internalHistory.submit(cmd))
            needRecalc = cmd.needsGuiRecalc
        for pDroneItemID in self.pDroneItemIDs:
            cmd = CalcChangeProjectedDroneProjectionRangeCommand(
                fitID=self.fitID,
                itemID=pDroneItemID,
                projectionRange=self.projectionRange)
            results.append(self.internalHistory.submit(cmd))
            needRecalc = True
        for pFighterPosition in self.pFighterPositions:
            cmd = CalcChangeProjectedFighterProjectionRangeCommand(
                fitID=self.fitID,
                position=pFighterPosition,
                projectionRange=self.projectionRange)
            results.append(self.internalHistory.submit(cmd))
            needRecalc = True
        for pFitID in self.pFitIDs:
            cmd = CalcChangeProjectedFitProjectionRangeCommand(
                fitID=self.fitID,
                projectedFitID=pFitID,
                projectionRange=self.projectionRange)
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
