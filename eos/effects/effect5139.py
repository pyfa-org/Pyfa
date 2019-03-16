# shipMiningBonusOREfrig1
#
# Used by:
# Variations of ship: Venture (3 of 3)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining"),
                                  "miningAmount", module.getModifiedItemAttr("shipBonusOREfrig1"),
                                  skill="Mining Frigate")
