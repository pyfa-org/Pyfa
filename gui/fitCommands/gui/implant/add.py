import wx

import eos.db
import gui.mainFrame
from eos.const import ImplantLocation
from gui import globalEvents as GE
from gui.fitCommands.calc.implant.add import CalcAddImplantCommand
from gui.fitCommands.calc.implant.changeLocation import CalcChangeImplantLocationCommand
from gui.fitCommands.helpers import ImplantInfo, InternalCommandHistory
from service.fit import Fit


class GuiAddImplantCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Add Implant')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        if fit.implantSource != ImplantLocation.FIT:
            cmd = CalcChangeImplantLocationCommand(fitID=self.fitID, source=ImplantLocation.FIT, commit=False)
            successSource = self.internalHistory.submit(cmd)
        else:
            successSource = False
        cmd = CalcAddImplantCommand(fitID=self.fitID, implantInfo=ImplantInfo(itemID=self.itemID), commit=False)
        successImplant = self.internalHistory.submit(cmd)
        eos.db.commit()
        sFit.recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        # Acceptable behavior when we already have passed implant and just switch source, or
        # when we have source and add implant, but not if we do not change anything
        return successSource or successImplant

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
