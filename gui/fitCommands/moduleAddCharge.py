import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE


class FitModuleAddChargeCommand(wx.Command):
    def __init__(self, fitID, itemID, modules):
        wx.Command.__init__(self, True, "Module Charge Add")
        # todo: evaluate mutaplasmid modules
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.itemID = itemID
        self.positions = {mod.modPosition: mod.chargeID for mod in modules}

    def Do(self):
        fit = self.sFit.getFit(self.fitID)
        self.sFit.setAmmo(self.fitID, self.itemID, [fit.modules[i] for i in self.positions.keys()])
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True

    def Undo(self):
        fit = self.sFit.getFit(self.fitID)
        for position, chargeID in self.positions.items():
            self.sFit.setAmmo(self.fitID, chargeID, [fit.modules[position]], False)
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID))
        return True
