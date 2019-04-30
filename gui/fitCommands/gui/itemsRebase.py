import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory
from service.fit import Fit
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.calc.itemRebase import CalcRebaseItemCommand
from gui.fitCommands.calc.module.changeCharges import CalcChangeModuleChargesCommand


class GuiRebaseItemsCommand(wx.Command):

    def __init__(self, fitID, rebaseMap):
        wx.Command.__init__(self, True, 'Rebase Items')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.rebaseMap = rebaseMap

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        for mod in fit.modules:
            if mod.itemID in self.rebaseMap:
                cmd = CalcRebaseItemCommand(
                    fitID=self.fitID,
                    containerName='modules',
                    position=fit.modules.index(mod),
                    itemID=self.rebaseMap[mod.itemID],
                    commit=False)
                self.internalHistory.submit(cmd)
            if mod.chargeID in self.rebaseMap:
                cmd = CalcChangeModuleChargesCommand(
                    fitID=self.fitID,
                    projected=False,
                    chargeMap={fit.modules.index(mod): self.rebaseMap[mod.chargeID]},
                    commit=False)
                self.internalHistory.submit(cmd)
        for containerName in ('drones', 'fighters', 'implants', 'boosters'):
            container = getattr(fit, containerName)
            for obj in container:
                if obj.itemID in self.rebaseMap:
                    cmd = CalcRebaseItemCommand(
                        fitID=self.fitID,
                        containerName=containerName,
                        position=container.index(obj),
                        itemID=self.rebaseMap[obj.itemID],
                        commit=False)
                    self.internalHistory.submit(cmd)
        # Need to process cargo separately as we want to merge items when needed,
        # e.g. FN iron and CN iron into single stack of CN iron
        for cargo in fit.cargo:
            if cargo.itemID in self.rebaseMap:
                amount = cargo.amount
                cmdRemove = CalcRemoveCargoCommand(
                    fitID=self.fitID,
                    cargoInfo=CargoInfo(itemID=cargo.itemID, amount=amount),
                    commit=False)
                cmdAdd = CalcAddCargoCommand(
                    fitID=self.fitID,
                    cargoInfo=CargoInfo(itemID=self.rebaseMap[cargo.itemID], amount=amount),
                    commit=False)
                self.internalHistory.submitBatch(cmdRemove, cmdAdd)
        eos.db.commit()
        sFit.recalc(fit)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return len(self.internalHistory) > 0

    def Undo(self):
        sFit = Fit.getInstance()
        success = self.internalHistory.undoAll()
        eos.db.commit()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
