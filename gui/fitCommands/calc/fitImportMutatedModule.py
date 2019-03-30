import wx
from eos.saveddata.module import Module
from eos.const import FittingModuleState
import eos.db
from eos.db.gamedata.queries import getDynamicItem
from logbook import Logger
from service.fit import Fit
pyfalog = Logger(__name__)


class FitImportMutatedCommand(wx.Command):
    """"
    Fitting command that takes info about mutated module, composes it and adds it to a fit
    """
    def __init__(self, fitID, baseItem, mutaItem, attrMap):
        wx.Command.__init__(self, True)
        self.fitID = fitID
        self.baseItem = baseItem
        self.mutaItem = mutaItem
        self.attrMap = attrMap
        self.new_position = None
        self.change = None
        self.replace_cmd = None

    def Do(self):
        sFit = Fit.getInstance()
        fitID = self.fitID
        if fitID is None:
            return False
        
        fit = eos.db.getFit(fitID)

        if self.baseItem is None:
            pyfalog.warning("Unable to build non-mutated module: no base item to build from")
            return False

        try:
            mutaTypeID = self.mutaItem.ID
        except AttributeError:
            mutaplasmid = None
        else:
            mutaplasmid = getDynamicItem(mutaTypeID)
        # Try to build simple item even though no mutaplasmid found
        if mutaplasmid is None:
            try:
                module = Module(self.baseItem)
            except ValueError:
                pyfalog.warning("Unable to build non-mutated module: {}", self.baseItem)
                return False
        # Build mutated module otherwise
        else:
            try:
                module = Module(mutaplasmid.resultingItem, self.baseItem, mutaplasmid)
            except ValueError:
                pyfalog.warning("Unable to build mutated module: {} {}", self.baseItem, self.mutaItem)
                return False
            else:
                for attrID, mutator in module.mutators.items():
                    if attrID in self.attrMap:
                        mutator.value = self.attrMap[attrID]


        # this is essentially the same as the FitAddModule command. possibly look into centralizing this functionality somewhere?
        if module.fits(fit):
            pyfalog.debug("Adding {} as module for fit {}", module, fit)
            module.owner = fit
            numSlots = len(fit.modules)
            fit.modules.append(module)
            if module.isValidState(FittingModuleState.ACTIVE):
                module.state = FittingModuleState.ACTIVE

            # todo: fix these
            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            # self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            sFit.checkStates(fit, module)

            # fit.fill()
            eos.db.commit()

            self.change = numSlots != len(fit.modules)
            self.new_position = module.modPosition
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
