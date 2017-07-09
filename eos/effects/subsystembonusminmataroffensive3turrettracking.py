# subsystemBonusMinmatarOffensive3TurretTracking
#
# Used by:
# Subsystem: Loki Offensive - Projectile Scoping Array
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "trackingSpeed", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive3"),
                                  skill="Minmatar Offensive Systems")
