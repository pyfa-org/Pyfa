# subsystemBonusMinmatarOffensiveProjectileWeaponMaxRange
#
# Used by:
# Subsystem: Loki Offensive - Turret Concurrence Registry
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive"), skill="Minmatar Offensive Systems")
