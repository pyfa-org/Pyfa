import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo, FighterInfo, BoosterInfo
from .calc.fitRemoveImplant import FitRemoveImplantCommand
from .calc.fitAddImplant import FitAddImplantCommand
from .calc.fitAddBooster import FitAddBoosterCommand
from .calc.fitRemoveCargo import FitRemoveCargoCommand
from .calc.fitAddCargo import FitAddCargoCommand
from .calc.fitReplaceModule import FitReplaceModuleCommand
from .calc.fitAddFighter import FitAddFighterCommand
from .calc.fitRemoveFighter import FitRemoveFighterCommand
from .calc.fitChangeDroneVariation import FitChangeDroneVariationCommand


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
                self.data.append(((FitReplaceModuleCommand, fitID, position, ModuleInfo(
                    itemID=itemID, chargeID=x.chargeID, state=x.state, spoolType=x.spoolType, spoolAmount=x.spoolAmount)),))
        elif context == 'implantItem':
            for x in selection:
                idx = fit.implants.index(x)
                state = x.active
                self.data.append(((FitRemoveImplantCommand, fitID, idx), (FitAddImplantCommand, fitID, itemID, state)))
        elif context == 'boosterItem':
            for x in selection:
                self.data.append(((FitAddBoosterCommand, fitID, BoosterInfo(
                    itemID=itemID, state=x.active, sideEffects={se.effectID: se.active for se in x.sideEffects})),))
        elif context == 'cargoItem':
            for x in selection:
                self.data.append(((FitRemoveCargoCommand, fitID, x.itemID, 1, True), (FitAddCargoCommand, fitID, itemID, x.amount)))
        elif context == 'fighterItem':
            for x in selection:
                fighterInfo = FighterInfo.fromFighter(x)
                fighterInfo.itemID = itemID
                self.data.append(((FitRemoveFighterCommand, fitID, fit.fighters.index(x)), (FitAddFighterCommand, fitID, fighterInfo)))
        elif context == 'droneItem':
            for x in selection:
                self.data.append(((FitChangeDroneVariationCommand, fitID, fit.drones.index(x), itemID),),)

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
