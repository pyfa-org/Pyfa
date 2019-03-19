import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from service.fit import Fit
from .calc.fitRebaseItem import FitRebaseItemCommand
from .calc.fitSetCharge import FitSetChargeCommand


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
            if mod.item is not None and mod.item.ID in self.rebaseMap:
                self.internal_history.Submit(FitRebaseItemCommand(self.fitID, "modules", mod.modPosition, self.rebaseMap[mod.item.ID]))
            if mod.charge is not None and mod.charge.ID in self.rebaseMap:
                self.internal_history.Submit(FitSetChargeCommand(self.fitID, [mod.modPosition], self.rebaseMap[mod.charge.ID]))
        for containerName in ("drones", "fighters", "implants", "boosters", "cargo"):
            container = getattr(fit, containerName)
            for obj in container:
                if obj.item is not None and obj.item.ID in self.rebaseMap:
                    self.internal_history.Submit(FitRebaseItemCommand(self.fitID, containerName, container.index(obj), self.rebaseMap[obj.item.ID]))
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
