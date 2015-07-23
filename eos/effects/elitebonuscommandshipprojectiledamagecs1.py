# eliteBonusCommandShipProjectileDamageCS1
#
# Used by:
# Ship: Sleipnir
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusCommandShips1"), skill="Command Ships")
