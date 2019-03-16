# shipHybridTracking1GD2
#
# Used by:
# Variations of ship: Catalyst (2 of 2)
# Ship: Algos
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGD2"), skill="Gallente Destroyer")
