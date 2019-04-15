import wx

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.module.changeCharges import CalcChangeModuleChargesCommand
from gui.fitCommands.calc.module.localAdd import CalcAddLocalModuleCommand
from gui.fitCommands.calc.module.localReplace import CalcReplaceLocalModuleCommand
from gui.fitCommands.helpers import InternalCommandHistory, ModuleInfo
from service.fit import Fit
from service.market import Market


class GuiAddLocalModuleCommand(wx.Command):

    def __init__(self, fitID, itemID, position=None):
        wx.Command.__init__(self, True, 'Add Local Module')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.position = position

    def Do(self):
        position = self.position
        success = False
        item = Market.getInstance().getItem(self.itemID)
        # Charge
        if item.isCharge and position is not None:
            cmd = CalcChangeModuleChargesCommand(fitID=self.fitID, projected=False, chargeMap={position: self.itemID})
            success = self.internalHistory.submit(cmd)
            if not success:
                Fit.getInstance().recalc(self.fitID)
                wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID))
                return False
        # Module to position
        elif position is not None:
            cmd = CalcReplaceLocalModuleCommand(fitID=self.fitID, position=position, newModInfo=ModuleInfo(itemID=self.itemID))
            success = self.internalHistory.submit(cmd)
            # Something went wrong with trying to fit the module into specific location, keep going to append it instead
            if not success:
                position = None
        # Module without position
        if position is None:
            cmd = CalcAddLocalModuleCommand(fitID=self.fitID, newModInfo=ModuleInfo(itemID=self.itemID))
            success = self.internalHistory.submit(cmd)
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='modadd', typeID=self.itemID) if success else GE.FitChanged(fitID=self.fitID))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(
            gui.mainFrame.MainFrame.getInstance(),
            GE.FitChanged(fitID=self.fitID, action='moddel', typeID=self.itemID) if success else GE.FitChanged(fitID=self.fitID))
        return success
