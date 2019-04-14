import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo, FighterInfo, BoosterInfo
from .calc.implant.remove import CalcRemoveImplantCommand
from .calc.implant.add import CalcAddImplantCommand
from .calc.booster.add import CalcAddBoosterCommand
from .calc.cargo.remove import CalcRemoveCargoCommand
from .calc.cargo.add import CalcAddCargoCommand
from .calc.module.localReplace import CalcReplaceLocalModuleCommand
from .calc.fighter.localAdd import CalcAddLocalFighterCommand
from .calc.fighter.localRemove import CalcRemoveLocalFighterCommand
from .calc.itemRebase import CalcRebaseItemCommand


class GuiMetaSwapCommand(wx.Command):
    def __init__(self, fitID, context, itemID, selection: list):
        wx.Command.__init__(self, True, "Meta Swap")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.internal_history = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.context = context
        self.data = []
        fit = self.sFit.getFit(fitID)

        if context == 'fittingModule':
            for x in selection:
                position = fit.modules.index(x)
                self.data.append(((CalcReplaceLocalModuleCommand, fitID, position, ModuleInfo(
                    itemID=itemID, chargeID=x.chargeID, state=x.state, spoolType=x.spoolType, spoolAmount=x.spoolAmount)),))
        elif context == 'implantItem':
            for x in selection:
                idx = fit.implants.index(x)
                state = x.active
                self.data.append(((CalcRemoveImplantCommand, fitID, idx), (CalcAddImplantCommand, fitID, itemID, state)))
        elif context == 'boosterItem':
            for x in selection:
                self.data.append(((CalcAddBoosterCommand, fitID, BoosterInfo(
                    itemID=itemID, state=x.active, sideEffects={se.effectID: se.active for se in x.sideEffects})),))
        elif context == 'cargoItem':
            for x in selection:
                self.data.append(((CalcRemoveCargoCommand, fitID, x.itemID, 1, True), (CalcAddCargoCommand, fitID, itemID, x.amount)))
        elif context == 'fighterItem':
            for x in selection:
                fighterInfo = FighterInfo.fromFighter(x)
                fighterInfo.itemID = itemID
                self.data.append(((CalcRemoveLocalFighterCommand, fitID, fit.fighters.index(x)), (CalcAddLocalFighterCommand, fitID, fighterInfo)))
        elif context == 'droneItem':
            for x in selection:
                self.data.append(((CalcRebaseItemCommand, fitID, 'drones', fit.drones.index(x), itemID),), )

    def Do(self):
        for cmds in self.data:
            for cmd in cmds:
                self.internal_history.Submit(cmd[0](*cmd[1:]))

        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
