import wx

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
        cmdImplant = CalcAddImplantCommand(fitID=self.fitID, implantInfo=ImplantInfo(itemID=self.itemID))
        cmdLocation = CalcChangeImplantLocationCommand(fitID=self.fitID, source=ImplantLocation.FIT)
        if self.internalHistory.submit(cmdImplant) and self.internalHistory.submit(cmdLocation):
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
