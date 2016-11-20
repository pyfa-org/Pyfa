# shipBonusTitanG2ROFBonus
#
# Used by:
# Variations of ship: Erebus (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "speed",
                                  src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
