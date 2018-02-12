# Not used by any item
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
# User-friendly name for the ability
from eos.modifiedAttributeDict import ModifiedAttributeDict

displayName = "Energy Neutralizer"
prefix = "fighterAbilityEnergyNeutralizer"
type = "active", "projected"
grouped = True


def handler(fit, src, context, **kwargs):
    if "projected" in context:
        amount = src.getModifiedItemAttr("{}Amount".format(prefix)) * src.amountActive
        time = src.getModifiedItemAttr("{}Duration".format(prefix))

        if 'effect' in kwargs:
            amount *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

        fit.addDrain(src, time, amount, 0)
