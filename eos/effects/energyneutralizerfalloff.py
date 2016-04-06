# energyNeutralizerFalloff
#
# Used by:
# Modules from group: Energy Neutralizer (51 of 51)
from eos.types import State
type = "active", "projected"
def handler(fit, container, context):
    if "projected" in context and ((hasattr(container, "state") \
    and container.state >= State.ACTIVE) or hasattr(container, "amountActive")):
        multiplier = container.amountActive if hasattr(container, "amountActive") else 1
        amount = container.getModifiedItemAttr("energyDestabilizationAmount")
        time = container.getModifiedItemAttr("duration")
        fit.addDrain(time, amount * multiplier, 0)
