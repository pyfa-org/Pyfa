import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localClone import CalcCloneLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, restoreRemovedDummies
from service.fit import Fit


class GuiCloneLocalModuleCommand(wx.Command):

    def __init__(self, fitID, srcPosition, dstPosition):
        wx.Command.__init__(self, True, 'Clone Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition
        self.savedItemID = None
        self.savedRemovedDummies = None

    def Do(self):
        if self.srcPosition == self.dstPosition:
            return False
        sFit = Fit.getInstance()
        cmd = CalcCloneLocalModuleCommand(fitID=self.fitID, srcPosition=self.srcPosition, dstPosition=self.dstPosition)
        success = self.internalHistory.submit(cmd)
        fit = sFit.getFit(self.fitID)
        if cmd.needsGuiRecalc:
            eos.db.flush()
            sFit.recalc(self.fitID)
        self.savedRemovedDummies = sFit.fill(self.fitID)
        eos.db.commit()
        self.savedItemID = fit.modules[self.srcPosition].itemID
        if success and self.savedItemID is not None:
            event = GE.FitChanged(fitIDs=(self.fitID,), action='modadd', typeID=self.savedItemID)
        else:
            event = GE.FitChanged(fitIDs=(self.fitID,))
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success

    def Undo(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        restoreRemovedDummies(fit, self.savedRemovedDummies)
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        if success and self.savedItemID is not None:
            event = GE.FitChanged(fitIDs=(self.fitID,), action='moddel', typeID=self.savedItemID)
        else:
            event = GE.FitChanged(fitIDs=(self.fitID,))
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), event)
        return success
