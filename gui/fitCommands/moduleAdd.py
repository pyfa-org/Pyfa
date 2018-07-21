import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
from .helpers import ModuleInfoCache


class FitModuleAddCommand(wx.Command):
    def __init__(self, fitID, itemID, position=None):
        wx.Command.__init__(self, True, "Module Add")
        # todo: evaluate mutaplasmid modules
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.sFit = Fit.getInstance()
        self.fitID = fitID
        self.itemID = itemID
        self.new_position = position
        self.old_mod = None

    def Do(self):
        change = None

        # if we have a position set, try to apply the module to that position
        if self.new_position:
            fit = self.sFit.getFit(self.fitID)
            old_mod = fit.modules[self.new_position]
            cache = ModuleInfoCache(old_mod.modPosition, old_mod.itemID, old_mod.state, old_mod.charge)
            change = self.sFit.changeModule(self.fitID, self.new_position, self.itemID)
            if change is None:
                # the new module doesn't fit in specified slot, remove the position
                self.new_position = None
            elif not old_mod.isEmpty:
                self.old_mod = cache

        # if we're not trying to set module to a position, simply append
        if not self.new_position:
            change, self.new_position = self.sFit.appendModule(self.fitID, self.itemID)

        if change is not None:
            print('new position: ',self.new_position )
            # self.slotsChanged() # unsure how to handle this right now? Perhaps move this to the event itself?
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="modadd", typeID=self.itemID))
            return True
        return False

    def Undo(self):
        if self.new_position:
            if self.old_mod:
                # we added a module on top of another one
                m = self.sFit.changeModule(self.fitID, self.old_mod.modPosition, self.old_mod.itemID, False)
                m.state = self.old_mod.state
                m.charge = self.old_mod.charge
            else:
                # todo: self.slotsChanged()
                # we simply added a module, so simply remove
                result = self.sFit.removeModule(self.fitID, [self.new_position])
            wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.fitID, action="moddel", typeID=self.itemID))
        return True
