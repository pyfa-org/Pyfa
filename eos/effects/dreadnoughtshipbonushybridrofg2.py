# dreadnoughtShipBonusHybridRoFG2
#
# Used by:
# Ship: Moros
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusG2"),
                                  skill="Gallente Dreadnought")
