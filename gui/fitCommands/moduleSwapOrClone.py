import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE


class FitModuleSwapOrCloneCommand(wx.Command):
    def __init__(self, fitID, srcPosition, dstPosition, clone=False):
        # todo: instead of modules, needs to be positions. Dead objects are a thing
        wx.Command.__init__(self, True, "Module State Change")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.srcPosition = srcPosition
        self.dstPosition = dstPosition
        self.clone = clone

    def Do(self):
        if self.clone:
            self.sFit.cloneModule(self.fitID, self.srcPosition, self.dstPosition)
        else:
            self.sFit.swapModules(self.fitID, self.srcPosition, self.dstPosition)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        if self.clone:
            # if we had cloned, the destinations was originally an empty slot, hence we can just remove the module
            self.sFit.removeModule(self.fitID, [self.dstPosition])
        else:
            self.sFit.swapModules(self.fitID, self.dstPosition, self.srcPosition)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
