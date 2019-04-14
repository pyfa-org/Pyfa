import wx
from logbook import Logger

import gui.mainFrame
from service.market import Market
from service.fit import Fit
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo
from .calcCommands.module.localAdd import CalcAddLocalModuleCommand
from .calcCommands.module.localReplace import CalcReplaceLocalModuleCommand
from .calcCommands.module.changeCharges import CalcChangeModuleChargesCommand


pyfalog = Logger(__name__)


class GuiModuleAddCommand(wx.Command):

    def __init__(self, fitID, itemID, position=None):
        """
        Handles adding an item, usually a module, to the Fitting Window.

        :param fitID: The fit ID that we are modifying
        :param itemID: The item that is to be added to the Fitting View. If this turns out to be a charge, we attempt to
                       set the charge on the underlying module (requires position)
        :param position: Optional. The position in fit.modules that we are attempting to set the item to
        """
        wx.Command.__init__(self, True, 'Module Add')
        self.fitID = fitID
        self.itemID = itemID
        self.position = position
        self.internalHistory = wx.CommandProcessor()

    def Do(self):
        pyfalog.debug("{} Do()".format(self))
        success = False
        item = Market.getInstance().getItem(self.itemID)
        # Charge
        if item.isCharge and self.position is not None:
            pyfalog.debug("Trying to add a charge")
            success = self.internalHistory.Submit(CalcChangeModuleChargesCommand(self.fitID, {self.position: self.itemID}))
            if not success:
                pyfalog.debug("    Failed")
                return False  # if it's a charge item and this failed, nothing more we can try.
        # Module to position
        elif self.position is not None:
            pyfalog.debug("Trying to add a module to a specific position")
            success = self.internalHistory.Submit(CalcReplaceLocalModuleCommand(
                fitID=self.fitID,
                position=self.position,
                newModInfo=ModuleInfo(itemID=self.itemID)))
            if not success:
                pyfalog.debug("    Failed")
                # something went wrong with trying to fit the module into specific location, attempt to append it
                self.position = None
        # Module without position
        if self.position is None:
            pyfalog.debug("Trying to append a module")
            success = self.internalHistory.Submit(CalcAddLocalModuleCommand(
                fitID=self.fitID,
                newModInfo=ModuleInfo(itemID=self.itemID)))

        if success:
            Fit.getInstance().recalc(self.fitID)
            wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID, action="modadd", typeID=self.itemID))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internalHistory.Commands:
            self.internalHistory.Undo()
        Fit.getInstance().recalc(self.fitID)
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitID=self.fitID, action="moddel", typeID=self.itemID))
        return True
