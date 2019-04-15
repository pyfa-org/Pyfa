import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.implant.add import CalcAddImplantCommand
from gui.fitCommands.helpers import ImplantInfo, InternalCommandHistory
from service.fit import Fit


class GuiSwapImplantMetaCommand(wx.Command):

    def __init__(self, fitID, position, itemID):
        wx.Command.__init__(self, True, 'Swap Implant Meta')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.position = position
        self.itemID = itemID

    def Do(self):
        sFit = Fit.getInstance()
        implant = sFit.getFit(self.fitID).implants[self.position]
        if implant.itemID == self.itemID:
            return False
        cmd = CalcAddImplantCommand(fitID=self.fitID, implantInfo=ImplantInfo(itemID=self.itemID, state=implant.active))
        if self.internalHistory.submit(cmd):
            sFit.recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
        return success
