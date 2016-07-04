# energyNeutralizerFalloff
#
# Used by:
# Modules from group: Energy Neutralizer (51 of 51)
from eos.types import State
type = "active", "projected"
def handler(fit, container, context):
    if "projected" in context and ((hasattr(container, "state") \
    and container.state >= State.ACTIVE) or hasattr(container, "amountActive")):
        amount = container.getModifiedItemAttr("energyNeutralizerAmount")
        time = container.getModifiedItemAttr("duration")
        fit.addDrain(time, amount, 0)


# TODO
# believe this doesn't actual require skills to use.
# Need to figure out how to remove the skill req *OR* tie it to the structure.`