import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.implant.add import CalcAddImplantCommand
from gui.fitCommands.helpers import ImplantInfo, InternalCommandHistory
from service.fit import Fit


class GuiAddImplantSetCommand(wx.Command):

    def __init__(self, fitID, itemIDs):
        wx.Command.__init__(self, True, 'Add Implant Set')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemIDs = itemIDs

    def Do(self):
        results = []
        for itemID in self.itemIDs:
            cmd = CalcAddImplantCommand(fitID=self.fitID, implantInfo=ImplantInfo(itemID=itemID))
            results.append(self.internalHistory.submit(cmd))
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        # Some might fail, as we already might have these implants
        return any(results)

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.flush()
        sFit = Fit.getInstance()
        sFit.recalc(self.fitID)
        sFit.fill(self.fitID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success
