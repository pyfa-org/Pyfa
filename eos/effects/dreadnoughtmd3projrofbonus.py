# dreadnoughtMD3ProjRoFBonus
#
# Used by:
# Ships named like: Naglfar (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Dreadnought").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusM3") * level)
