# subsystemBonusMinmatarOffensive2ProjectileWeaponDamageMultiplier
#
# Used by:
# Subsystem: Loki Offensive - Projectile Scoping Array
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive2"),
                                  skill="Minmatar Offensive Systems")
