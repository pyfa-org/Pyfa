import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from collections import namedtuple


ModuleInfoCache = namedtuple('ModuleInfoCache', ['modPosition', 'itemID', 'state', 'charge'])

class FitModuleRemoveCommand(wx.Command):
    def __init__(self, fitID, modules):
        # todo: evaluate mutaplasmid modules
        wx.Command.__init__(self, True, "Module Remove")
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.modCache = [ModuleInfoCache(mod.modPosition, mod.item.ID, mod.state, mod.charge) for mod in modules]

    def Do(self):
        self.sFit.getFit(self.fitID)
        result = self.sFit.removeModule(self.fitID, [mod.modPosition for mod in self.modCache])

        if result is not None:
            # self.slotsChanged() # todo: fix
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=set([mod.itemID for mod in self.modCache])))
        return True

    def Undo(self):
        for mod in self.modCache:
            m = self.sFit.changeModule(self.fitID, mod.modPosition, mod.itemID, False)
            m.state = mod.state
            m.charge = mod.charge
        self.sFit.recalc(self.fitID)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd", typeID=set([mod.itemID for mod in self.modCache])))

        return True
