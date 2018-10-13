import wx
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
from service.fit import Fit
pyfalog = Logger(__name__)


class FitAddModuleCommand(wx.Command):
    """"
    Fitting command that appends a module to a fit using the first available slot. In the case of a Subsystem, it checks
    if there is already a subsystem with the same slot, and runs the replace command instead.

    from sFit.appendModule
    """
    def __init__(self, fitID, itemID, mutaplasmidID=None, baseID=None):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.itemID = itemID
        self.mutaplasmidID = mutaplasmidID
        self.baseID = baseID
        self.new_position = None
        self.change = None
        self.replace_cmd = None

    def Do(self):
        sFit = Fit.getInstance()
        fitID = self.fitID
        itemID = self.itemID
        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))

        bItem = eos.db.getItem(self.baseID) if self.baseID else None
        mItem = next((x for x in bItem.mutaplasmids if x.ID == self.mutaplasmidID)) if self.mutaplasmidID else None

        try:
            self.module = Module(item, bItem, mItem)
        except ValueError:
            pyfalog.warning("Invalid module: {}", item)
            return False

        # If subsystem and we need to replace, run the replace command instead and bypass the rest of this command
        if self.module.item.category.name == "Subsystem":
            for mod in fit.modules:
                if mod.getModifiedItemAttr("subSystemSlot") == self.module.getModifiedItemAttr("subSystemSlot"):
                    from .fitReplaceModule import FitReplaceModuleCommand
                    self.replace_cmd = FitReplaceModuleCommand(self.fitID, mod.modPosition, itemID)
                    return self.replace_cmd.Do()

        if self.module.fits(fit):
            pyfalog.debug("Adding {} as module for fit {}", self.module, fit)
            self.module.owner = fit
            numSlots = len(fit.modules)
            fit.modules.append(self.module)
            if self.module.isValidState(State.ACTIVE):
                self.module.state = State.ACTIVE

            # todo: fix these
            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            # self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            sFit.checkStates(fit, self.module)

            # fit.fill()
            eos.db.commit()

            self.change = numSlots != len(fit.modules)
            self.new_position = self.module.modPosition
        else:
            return False

        return True

    def Undo(self):
        # We added a subsystem module, which actually ran the replace command. Run the undo for that guy instead
        if self.replace_cmd:
            return self.replace_cmd.Undo()

        from .fitRemoveModule import FitRemoveModuleCommand  # Avoid circular import
        if self.new_position:
            cmd = FitRemoveModuleCommand(self.fitID, [self.new_position])
            cmd.Do()
        return True
