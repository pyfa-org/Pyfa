# fighterAbilityECM
#
# Used by:
# Fighters named like: Scarab (4 of 4)
"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
from eos.modifiedAttributeDict import ModifiedAttributeDict

# User-friendly name for the ability
displayName = "ECM"

prefix = "fighterAbilityECM"

type = "projected", "active"
grouped = True


def handler(fit, module, context, **kwargs):
    if "projected" not in context:
        return
    # jam formula: 1 - (1- (jammer str/ship str))^(# of jam mods with same str))
    strModifier = 1 - (module.getModifiedItemAttr("{}Strength{}".format(prefix, fit.scanType)) * module.amountActive) / fit.scanStrength

    if 'effect' in kwargs:
        strModifier *= ModifiedAttributeDict.getResistance(fit, kwargs['effect'])

    fit.ecmProjectedStr *= strModifier
