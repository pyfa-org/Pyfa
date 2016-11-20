# dreadnoughtShipBonusHybridDmgG1
#
# Used by:
# Ship: Moros
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("dreadnoughtShipBonusG1"),
                                  skill="Gallente Dreadnought")
