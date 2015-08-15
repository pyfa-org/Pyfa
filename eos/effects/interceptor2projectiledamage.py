# interceptor2ProjectileDamage
#
# Used by:
# Ship: Claw
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", ship.getModifiedItemAttr("eliteBonusInterceptor2"), skill="Interceptors")
