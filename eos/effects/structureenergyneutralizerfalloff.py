# structureEnergyNeutralizerFalloff
#
# Used by:
# Structure Modules from group: Structure Energy Neutralizer (5 of 5)
from eos.saveddata.module import State

type = "active", "projected"


def handler(fit, container, context):
    amount = 0
    if "projected" in context:
        if (hasattr(container, "state") and container.state >= State.ACTIVE) or hasattr(container, "amountActive"):
            amount = container.getModifiedItemAttr("energyNeutralizerAmount")
            time = container.getModifiedItemAttr("duration")
            fit.addDrain(container, time, amount, 0)
