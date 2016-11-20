# Not used by any item
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
# User-friendly name for the ability
displayName = "Energy Neutralizer"
prefix = "fighterAbilityEnergyNeutralizer"
type = "active", "projected"


def handler(fit, src, context):
    if "projected" in context:
        amount = src.getModifiedItemAttr("{}Amount".format(prefix))
        time = src.getModifiedItemAttr("{}Duration".format(prefix))

        fit.addDrain(src, time, amount, 0)
