# dreadnoughtMD3ProjRoFBonus
#
# Used by:
# Ship: Naglfar
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusM3"), skill="Minmatar Dreadnought")
