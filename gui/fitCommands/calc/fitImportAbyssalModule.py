import wx
from eos.saveddata.module import Module, State
import eos.db
from logbook import Logger
from service.fit import Fit
pyfalog = Logger(__name__)


class FitImportAbyssalCommand(wx.Command):
    """"
    Fitting command that takes in a complete Abyssal module and adds it to a fit
    """
    def __init__(self, fitID, module):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.module = module
        self.new_position = None
        self.change = None
        self.replace_cmd = None

    def Do(self):
        sFit = Fit.getInstance()
        fitID = self.fitID
        fit = eos.db.getFit(fitID)

        # this is essentially the same as the FitAddModule command. possibly look into centralizing this functionality somewhere?
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
        if self.new_position is not None:
            cmd = FitRemoveModuleCommand(self.fitID, [self.new_position])
            cmd.Do()
        return True
