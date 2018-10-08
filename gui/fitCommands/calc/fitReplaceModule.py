import wx
from logbook import Logger

import eos.db
from eos.saveddata.module import Module, State
from gui.fitCommands.helpers import ModuleInfoCache

pyfalog = Logger(__name__)


class FitReplaceModuleCommand(wx.Command):
    """"
    Fitting command that changes an existing module into another.

    from sFit.changeModule
    """
    def __init__(self, fitID, position, itemID):
        wx.Command.__init__(self, True, "Change Module")
        self.fitID = fitID
        self.itemID = itemID
        self.position = position
        self.module = None  # the module version of itemID
        self.old_module = None

    def Do(self):
        return self.change_module(self.fitID, self.position, self.itemID)

    def Undo(self):
        if self.old_module is None:
            fit = eos.db.getFit(self.fitID)
            fit.modules.toDummy(self.position)
            return True

        self.change_module(self.fitID, self.position, self.old_module.itemID)
        self.module.state = self.old_module.state
        self.module.charge = self.old_module.charge
        return True

    def change_module(self, fitID, position, itemID):
        fit = eos.db.getFit(fitID)

        # We're trying to add a charge to a slot, which won't work. Instead, try to add the charge to the module in that slot.
        # todo: evaluate if this is still a thing
        # actually, this seems like it should be handled higher up...
        #
        # if self.isAmmo(itemID):
        #     module = fit.modules[self.position]
        #     if not module.isEmpty:
        #         self.setAmmo(fitID, itemID, [module])
        #     return True

        pyfalog.debug("Changing position of module from position ({0}) for fit ID: {1}", self.position, fitID)

        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))

        mod = fit.modules[self.position]
        if not mod.isEmpty:
            self.old_module = ModuleInfoCache(mod.modPosition, mod.item.ID, mod.state, mod.charge, mod.baseItemID, mod.mutaplasmidID)

        try:
            self.module = Module(item)
        except ValueError:
            pyfalog.warning("Invalid item: {0}", itemID)
            return False

        if self.module.slot != mod.slot:
            return False

        # Dummy it out in case the next bit fails
        fit.modules.toDummy(self.position)

        if self.module.fits(fit):
            self.module.owner = fit
            fit.modules.toModule(self.position, self.module)
            if self.module.isValidState(State.ACTIVE):
                self.module.state = State.ACTIVE

            # Then, check states of all modules and change where needed. This will recalc if needed
            # self.checkStates(fit, m)

            # fit.fill()
            eos.db.commit()
            return True
        return False
