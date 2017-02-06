# shipBonusDreadnoughtG2ROFBonus
#
# Used by:
# Variations of ship: Moros (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "speed",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtG2"), skill="Gallente Dreadnought")
