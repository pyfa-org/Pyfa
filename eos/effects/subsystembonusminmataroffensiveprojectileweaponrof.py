# subsystemBonusMinmatarOffensiveProjectileWeaponROF
#
# Used by:
# Subsystem: Loki Offensive - Covert Reconfiguration
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "speed", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive"),
                                  skill="Minmatar Offensive Systems")
