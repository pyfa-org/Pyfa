import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import CargoInfo
from service.fit import Fit
from .calc.itemRebase import FitRebaseItemCommand
from .calc.module.changeCharges import FitChangeModuleChargesCommand
from .calc.cargo.add import FitAddCargoCommand
from .calc.cargo.remove import FitRemoveCargoCommand



class GuiRebaseItemsCommand(wx.Command):

    def __init__(self, fitID, rebaseMap):
        wx.Command.__init__(self, True, "Mass Rebase Item")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.fitID = fitID
        self.rebaseMap = rebaseMap
        self.internal_history = wx.CommandProcessor()

    def Do(self):
        fit = eos.db.getFit(self.fitID)
        for mod in fit.modules:
            if mod.itemID in self.rebaseMap:
                self.internal_history.Submit(FitRebaseItemCommand(fitID=self.fitID, containerName="modules", position=mod.modPosition, itemID=self.rebaseMap[mod.itemID], commit=False))
            if mod.chargeID in self.rebaseMap:
                self.internal_history.Submit(FitChangeModuleChargesCommand(fitID=self.fitID, chargeMap={mod.modPosition: self.rebaseMap[mod.chargeID]}))
        for containerName in ("drones", "fighters", "implants", "boosters"):
            container = getattr(fit, containerName)
            for obj in container:
                if obj.itemID in self.rebaseMap:
                    self.internal_history.Submit(FitRebaseItemCommand(fitID=self.fitID, containerName=containerName, position=container.index(obj), itemID=self.rebaseMap[obj.itemID], commit=False))
        # Need to process cargo separately as we want to merge items when needed,
        # e.g. FN iron and CN iron into single stack of CN iron
        for cargo in fit.cargo:
            if cargo.itemID in self.rebaseMap:
                amount = cargo.amount
                self.internal_history.Submit(FitRemoveCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=cargo.itemID, amount=amount)))
                self.internal_history.Submit(FitAddCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.rebaseMap[cargo.itemID], amount=amount)))
        if self.internal_history.Commands:
            eos.db.commit()
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
            return True
        else:
            return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
