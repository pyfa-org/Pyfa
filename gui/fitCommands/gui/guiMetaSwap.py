import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo, FighterInfo, BoosterInfo
from gui.fitCommands.calc.implant.remove import CalcRemoveImplantCommand
from gui.fitCommands.calc.implant.add import CalcAddImplantCommand
from gui.fitCommands.calc.booster.add import CalcAddBoosterCommand
from gui.fitCommands.calc.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.calc.cargo.add import CalcAddCargoCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.calc.fighter.localAdd import CalcAddLocalFighterCommand
from gui.fitCommands.calc.fighter.localRemove import CalcRemoveLocalFighterCommand
from gui.fitCommands.calc.itemRebase import CalcRebaseItemCommand


class GuiMetaSwapCommand(wx.Command):
    def __init__(self, fitID, context, itemID, selection: list):
        wx.Command.__init__(self, True, "Meta Swap")
        self.internalHistory = wx.CommandProcessor()
        self.fitID = fitID
        self.itemID = itemID
        self.context = context
        self.data = []
        fit = Fit.getInstance().getFit(fitID)

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
                self.internalHistory.Submit(cmd[0](*cmd[1:]))

        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
