import wx
from logbook import Logger

import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.helpers import ModuleInfo
from service.fit import Fit
from .calc.fitAddModule import FitAddModuleCommand


pyfalog = Logger(__name__)


class GuiFillWithModuleCommand(wx.Command):
    def __init__(self, fitID, itemID, position=None):
        """
        Handles adding an item, usually a module, to the Fitting Window.

        :param fitID: The fit ID that we are modifying
        :param itemID: The item that is to be added to the Fitting View. If this turns out to be a charge, we attempt to
                       set the charge on the underlying module (requires position)
        :param position: Optional. The position in fit.modules that we are attempting to set the item to
        """
        wx.Command.__init__(self, True, "Module Fill: {}".format(itemID))
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.itemID = itemID
        self.internal_history = wx.CommandProcessor()
        self.position = position
        self.old_mod = None

    def Do(self):
        pyfalog.debug("{} Do()".format(self))
        pyfalog.debug("Trying to append a module")
        added_modules = 0
        while self.internal_history.Submit(FitAddModuleCommand(fitID=self.fitID, newModInfo=ModuleInfo(itemID=self.itemID))):
            added_modules += 1

        if added_modules > 0:
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
