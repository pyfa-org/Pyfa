import wx

import eos.db
import gui.mainFrame
from eos.const import ImplantLocation
from gui import globalEvents as GE
from gui.fitCommands.calc.implant.add import CalcAddImplantCommand
from gui.fitCommands.calc.implant.changeLocation import CalcChangeImplantLocationCommand
from gui.fitCommands.helpers import ImplantInfo, InternalCommandHistory
from service.fit import Fit


class GuiImportImplantsCommand(wx.Command):

    def __init__(self, fitID, implants):
        wx.Command.__init__(self, True, 'Import Implants')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.implants = set(i[0] for i in implants)

    def Do(self):
        if not self.implants:
            return False
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        if fit.implantSource != ImplantLocation.FIT:
            cmd = CalcChangeImplantLocationCommand(fitID=self.fitID, source=ImplantLocation.FIT)
            successSource = self.internalHistory.submit(cmd)
        else:
            successSource = False
        resultsImplants = []
        for itemID in self.implants:
            cmd = CalcAddImplantCommand(fitID=self.fitID, implantInfo=ImplantInfo(itemID=itemID))
            resultsImplants.append(self.internalHistory.submit(cmd))
        successImplants = any(resultsImplants)
        # Acceptable behavior when we already have passed implant and just switch source, or
        # when we have source and add implant, but not if we do not change anything
        success = successSource or successImplants
        eos.db.flush()
        sFit = Fit.getInstance()
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
