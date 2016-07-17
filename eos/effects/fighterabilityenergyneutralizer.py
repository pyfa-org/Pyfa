# Not used by any item
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
from eos.types import State

# User-friendly name for the ability
displayName = "Energy Neutralizer"

prefix = "fighterAbilityEnergyNeutralizer"

type = "active", "projected"

def handler(fit, module, context):
    if "projected" in context:
        amount = module.getModifiedItemAttr("{}Amount".format(prefix))
        time = module.getModifiedItemAttr("{}Duration".format(prefix))
        rigSize = fit.ship.getModifiedItemAttr("rigSize")
        modifierLarge = module.getModifiedItemAttr("entityCapacitorLevelModifierLarge")
        modifierMedium = module.getModifiedItemAttr("entityCapacitorLevelModifierMedium")
        modifierSmall = module.getModifiedItemAttr("entityCapacitorLevelModifierSmall")

        # Small rigged ships
        if (rigSize == 1) and modifierSmall:
            amount = amount * modifierSmall

        # Medium rigged ships
        if (rigSize == 2) and modifierMedium:
            amount = amount * modifierMedium

        # Large rigged ships
        if (rigSize == 3) and modifierLarge:
            amount = amount * modifierLarge

        fit.addDrain(time, amount, 0)