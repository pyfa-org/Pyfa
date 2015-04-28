# shipBonusDroneDamageMultiplierGC2
#
# Used by:
# Ships named like: Stratios (2 of 2)
# Ship: Vexor
# Ship: Vexor Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC2") * level)
