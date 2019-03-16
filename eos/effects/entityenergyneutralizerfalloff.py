# entityEnergyNeutralizerFalloff
#
# Used by:
# Drones from group: Energy Neutralizer Drone (3 of 3)
from eos.const import FittingModuleState
from eos.modifiedAttributeDict import ModifiedAttributeDict

type = "active", "projected"


def handler(fit, src, context, **kwargs):
    if "projected" in context and ((hasattr(src, "state") and src.state >= FittingModuleState.ACTIVE) or
                                   hasattr(src, "amountActive")):
        amount = src.getModifiedItemAttr("energyNeutralizerAmount")
        time = src.getModifiedItemAttr("energyNeutralizerDuration")

        if 'effect' in kwargs:
            amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

        fit.addDrain(src, time, amount, 0)
