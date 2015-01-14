# shipBonusDroneDamageMultiplierGC2
#
# Used by:
# Ships named like: Stratios (2 of 2)
# Variations of ship: Vexor (3 of 4)
# Ship: Vexor Quafe Edition
# Ship: 伊什塔级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGC2") * level)
