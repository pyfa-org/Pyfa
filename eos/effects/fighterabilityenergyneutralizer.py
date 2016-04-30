"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
from eos.types import State

# User-friendly name for the ability
displayName = "Energy Neutralizer"

prefix = "fighterAbilityEnergyNeutralizer"

type = "active", "projected"

def handler(fit, container, context):
    if "projected" in context and ((hasattr(container, "state") and container.state >= State.ACTIVE) or hasattr(container, "amountActive")):
        multiplier = container.amountActive if hasattr(container, "amountActive") else 1
        amount = container.getModifiedItemAttr("{}Amount".format(prefix))
        time = container.getModifiedItemAttr("{}Duration".format(prefix))
        fit.addDrain(time, amount * multiplier, 0)