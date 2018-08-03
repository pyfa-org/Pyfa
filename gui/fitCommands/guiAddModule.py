import wx

import gui.mainFrame
from service.fit import Fit
from gui import globalEvents as GE
from .calc.fitAddModule import FitAddModuleCommand
from .calc.fitReplaceModule import FitReplaceModuleCommand

class GuiModuleAddCommand(wx.Command):
    def __init__(self, fitID, itemID, position=None):
        wx.Command.__init__(self, True, "Module Add")
        # todo: evaluate mutaplasmid modules
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.itemID = itemID
        self.internal_history = wx.CommandProcessor()
        self.new_position = position
        self.old_mod = None

    def Do(self):
        success = False
        # if we have a position set, try to apply the module to that position

        # todo: check to see if item is a charge. if it is, dont try to add module, but instead set ammo
        if self.new_position:
            success = self.internal_history.Submit(FitReplaceModuleCommand(self.fitID, self.new_position, self.itemID))
            if not success:
                # something went wrong with trying to fit the module into specific location, attemp to append it
                self.new_position = None

        # if we're not trying to set module to a position, simply append
        if not self.new_position:
            success = self.internal_history.Submit(FitAddModuleCommand(self.fitID, self.itemID))

        if success:
            self.sFit.recalc(self.fitID)
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd", typeID=self.itemID))
            return True
        return False

        #
        # if change is not None:
        #     print('new position: ',self.new_position )
        #     # self.slotsChanged() # unsure how to handle this right now? Perhaps move this to the event itself?
        #     return True
        # return False

    def Undo(self):
        for _ in self.internal_history.Commands:
            self.internal_history.Undo()
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=self.itemID))
        return True
