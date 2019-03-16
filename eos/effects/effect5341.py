# shipHybridDmg1GBC1
#
# Used by:
# Variations of ship: Brutix (3 of 3)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("shipBonusGBC1"),
                                  skill="Gallente Battlecruiser")
