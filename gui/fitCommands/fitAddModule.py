import wx
from service.fit import Fit

import gui.mainFrame
from gui import globalEvents as GE
#from .helpers import ModuleInfoCache
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
pyfalog = Logger(__name__)


class FitAddModuleCommand(wx.Command):
    """"
    Fitting command that appends a module to a fit using the first available slot.

    from sFit.appendModule
    """
    def __init__(self, fitID, itemID):
        wx.Command.__init__(self, True, "Module Add")
        self.fitID = fitID
        self.itemID = itemID
        self.new_position = None
        self.change = None

    def Do(self):
        fitID = self.fitID
        itemID = self.itemID
        pyfalog.debug("Appending module for fit ({0}) using item: {1}", fitID, itemID)
        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))

        try:
            self.module = Module(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", itemID)
            return False

        if self.module.item.category.name == "Subsystem":
            fit.modules.freeSlot(self.module.getModifiedItemAttr("subSystemSlot"))

        if self.module.fits(fit):
            self.module.owner = fit
            numSlots = len(fit.modules)
            fit.modules.append(self.module)
            if self.module.isValidState(State.ACTIVE):
                self.module.state = State.ACTIVE

            # todo: fix these
            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            # self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            # self.checkStates(fit, m)

            fit.fill()
            eos.db.commit()

            self.change = numSlots != len(fit.modules)
            self.new_position = self.module.modPosition
        else:
            return False

        return True

    def Undo(self):
        from .fitRemoveModule import FitRemoveModuleCommand  # Avoid circular import
        if self.new_position:
            cmd = FitRemoveModuleCommand(self.fitID, [self.new_position])
            cmd.Do()
        return True
