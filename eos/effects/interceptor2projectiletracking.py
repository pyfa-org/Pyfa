# Used by:
# Ship: Claw
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Interceptors").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                    "trackingSpeed", ship.getModifiedItemAttr("eliteBonusInterceptor2") * level)