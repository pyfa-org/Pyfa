import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit


class GuiFillWithLocalModulesCommand(wx.Command):

    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, 'Fill with Local Modules')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID

    def Do(self):
        added_modules = 0
        while self.internalHistory.submit(CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=ModuleInfo(itemID=self.itemID))):
            added_modules += 1
        if added_modules > 0:
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.itemID))
            return True
        return False

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.itemID))
        return success
