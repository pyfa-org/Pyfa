import wx
from logbook import Logger

from gui.fitCommands.helpers import restoreCheckedStates
from service.fit import Fit
from service.market import Market


pyfalog = Logger(__name__)


class CalcChangeModuleChargesCommand(wx.Command):

    def __init__(self, fitID, projected, chargeMap, ignoreRestrictions=False, recalc=True):
        wx.Command.__init__(self, True, 'Change Module Charges')
        self.fitID = fitID
        self.projected = projected
        self.chargeMap = chargeMap
        self.ignoreRestriction = ignoreRestrictions
        self.recalc = recalc
        self.savedChargeMap = None
        self.savedStateCheckChanges = None

    def Do(self):
        pyfalog.debug('Doing change of module charges according to map {} on fit {}'.format(self.chargeMap, self.fitID))
        sFit = Fit.getInstance()
        fit = sFit.getFit(self.fitID)
        container = fit.modules if not self.projected else fit.projectedModules
        changes = False
        self.savedChargeMap = {}
        sMkt = Market.getInstance()
        for position, chargeItemID in self.chargeMap.items():
            mod = container[position]
            if mod.isEmpty:
                continue
            if mod.chargeID is None and chargeItemID is None:
                continue
            if mod.chargeID == chargeItemID:
                continue
            chargeItem = sMkt.getItem(chargeItemID) if chargeItemID is not None else None
            if chargeItem is not None and not chargeItem.isCharge:
                continue
            if not self.ignoreRestriction and not mod.isValidCharge(chargeItem):
                pyfalog.warning('Invalid charge {} for {}'.format(chargeItem, mod))
                continue
            pyfalog.debug('Setting charge {} for {} on fit {}'.format(chargeItem, mod, self.fitID))
            self.savedChargeMap[position] = mod.chargeID
            changes = True
            mod.charge = chargeItem
        if not changes:
            return False
        if self.recalc:
            sFit.recalc(fit)
            self.savedStateCheckChanges = sFit.checkStates(fit, None)
        return True

    def Undo(self):
        pyfalog.debug('Undoing change of module charges according to map {} on fit {}'.format(self.chargeMap, self.fitID))
        cmd = CalcChangeModuleChargesCommand(
            fitID=self.fitID,
            projected=self.projected,
            chargeMap=self.savedChargeMap,
            ignoreRestrictions=True,
            recalc=False)
        if not cmd.Do():
            return False
        restoreCheckedStates(Fit.getInstance().getFit(self.fitID), self.savedStateCheckChanges)
        return True

    @property
    def needsGuiRecalc(self):
        if self.savedStateCheckChanges is None:
            return True
        for container in self.savedStateCheckChanges:
            if len(container) > 0:
                return True
        return False
