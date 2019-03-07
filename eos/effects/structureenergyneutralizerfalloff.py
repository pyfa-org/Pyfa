# structureEnergyNeutralizerFalloff
#
# Used by:
# Structure Modules from group: Structure Energy Neutralizer (5 of 5)
from eos.saveddata.module import FittingModuleState
from eos.modifiedAttributeDict import ModifiedAttributeDict

type = "active", "projected"


def handler(fit, src, context, **kwargs):
    amount = 0
    if "projected" in context:
        if (hasattr(src, "state") and src.state >= FittingModuleState.ACTIVE) or hasattr(src, "amountActive"):
            amount = src.getModifiedItemAttr("energyNeutralizerAmount")

            if 'effect' in kwargs:
                amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

            time = src.getModifiedItemAttr("duration")

            fit.addDrain(src, time, amount, 0)