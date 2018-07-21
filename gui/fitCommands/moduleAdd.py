import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE


class FitModuleAddCommand(wx.Command):
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Module Add")
        # todo: evaluate mutaplasmid modules
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.itemID = itemID
        self.new_position = None

    def Do(self):
        # todo: figure how not to add this command to stack if module doesn't fit correctly.
        populate, self.new_position = self.sFit.appendModule(self.fitID, self.itemID)
        if populate is not None:
            # self.slotsChanged() # unsure how to handle this right now? Perhaps move this to the event itself?
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd", typeID=self.itemID))
        return True

    def Undo(self):
        if (self.new_position):
            # todo: self.slotsChanged()
            result = self.sFit.removeModule(self.fitID, [self.new_position])
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=self.itemID))
        return True
