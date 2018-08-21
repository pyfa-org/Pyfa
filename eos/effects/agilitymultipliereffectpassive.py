# agilityMultiplierEffectPassive
#
# Used by:
# Modules named like: Polycarbon Engine Housing (8 of 8)
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("agilityBonus"), stackingPenalties=True)
