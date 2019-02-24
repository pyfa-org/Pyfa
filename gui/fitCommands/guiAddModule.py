import wx
import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from .calc.fitAddModule import FitAddModuleCommand
from .calc.fitReplaceModule import FitReplaceModuleCommand
from .calc.fitSetCharge import FitSetChargeCommand
from service.fit import Fit
from logbook import Logger
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
        wx.Command.__init__(self, True, "Module Add: {}".format(itemID))
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.itemID = itemID
        self.internal_history = wx.CommandProcessor()
        self.position = position
        self.old_mod = None

    def Do(self):
        pyfalog.debug("{} Do()".format(self))
        success = False
        item = eos.db.getItem(self.itemID)
        if item.isCharge and self.position is not None:
            pyfalog.debug("Trying to add a charge")
            success = self.internal_history.Submit(FitSetChargeCommand(self.fitID, [self.position], self.itemID))
            if not success:
                pyfalog.debug("    Failed")
                return False  # if it's a charge item and this failed, nothing more we can try.
        # if we have a position set, try to apply the module to that position
        elif self.position is not None:
            pyfalog.debug("Trying to add a module to a specific position")
            success = self.internal_history.Submit(FitReplaceModuleCommand(self.fitID, self.position, self.itemID))
            if not success:
                pyfalog.debug("    Failed")
                # something went wrong with trying to fit the module into specific location, attempt to append it
                self.position = None

        # if we're not trying to set module to a position, simply append
        if self.position is None:
            pyfalog.debug("Trying to append a module")
            success = self.internal_history.Submit(FitAddModuleCommand(self.fitID, self.itemID))

        if success:
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd", typeID=self.itemID))
            return True
        return False

    def Undo(self):
        pyfalog.debug("{} Undo()".format(self))
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=self.itemID))
        return True
