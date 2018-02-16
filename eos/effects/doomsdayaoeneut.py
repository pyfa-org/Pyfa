# doomsdayAOENeut
#
# Used by:
# Module: Energy Neutralization Burst Projector
from eos.saveddata.module import State
from eos.modifiedAttributeDict import ModifiedAttributeDict

type = "active", "projected"


def handler(fit, src, context, **kwargs):
    if "projected" in context and ((hasattr(src, "state") and src.state >= State.ACTIVE) or
                                    hasattr(src, "amountActive")):
        amount = src.getModifiedItemAttr("energyNeutralizerAmount")

        if 'effect' in kwargs:
            amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

        time = src.getModifiedItemAttr("duration")

        fit.addDrain(src, time, amount, 0)
