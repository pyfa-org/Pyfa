# Used by:
# Ship: Naglfar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Dreadnought").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("dreadnoughtShipBonusM1") * level)
