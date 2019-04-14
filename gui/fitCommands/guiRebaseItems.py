import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import CargoInfo
from service.fit import Fit
from .calcCommands.itemRebase import CalcRebaseItemCommand
from .calcCommands.module.changeCharges import CalcChangeModuleChargesCommand
from .calcCommands.cargo.add import CalcAddCargoCommand
from .calcCommands.cargo.remove import CalcRemoveCargoCommand
from gui.fitCommands.helpers import InternalCommandHistory



class GuiRebaseItemsCommand(wx.Command):

    def __init__(self, fitID, rebaseMap):
        wx.Command.__init__(self, True, "Mass Rebase Item")
        self.fitID = fitID
        self.rebaseMap = rebaseMap
        self.internalHistory = InternalCommandHistory()

    def Do(self):
        fit = eos.db.getFit(self.fitID)
        for mod in fit.modules:
            if mod.itemID in self.rebaseMap:
                self.internalHistory.submit(CalcRebaseItemCommand(fitID=self.fitID, containerName="modules", position=mod.modPosition, itemID=self.rebaseMap[mod.itemID], commit=False))
            if mod.chargeID in self.rebaseMap:
                self.internalHistory.submit(CalcChangeModuleChargesCommand(fitID=self.fitID, chargeMap={mod.modPosition: self.rebaseMap[mod.chargeID]}))
        for containerName in ("drones", "fighters", "implants", "boosters"):
            container = getattr(fit, containerName)
            for obj in container:
                if obj.itemID in self.rebaseMap:
                    self.internalHistory.submit(CalcRebaseItemCommand(fitID=self.fitID, containerName=containerName, position=container.index(obj), itemID=self.rebaseMap[obj.itemID], commit=False))
        # Need to process cargo separately as we want to merge items when needed,
        # e.g. FN iron and CN iron into single stack of CN iron
        for cargo in fit.cargo:
            if cargo.itemID in self.rebaseMap:
                amount = cargo.amount
                self.internalHistory.submit(CalcRemoveCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=cargo.itemID, amount=amount)))
                self.internalHistory.submit(CalcAddCargoCommand(fitID=self.fitID, cargoInfo=CargoInfo(itemID=self.rebaseMap[cargo.itemID], amount=amount)))
        if self.internalHistory:
            eos.db.commit()
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        else:
            return False

    def Undo(self):
        self.internalHistory.undoAll()
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return True
