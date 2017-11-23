# subsystemMPTFittingReduction
#
# Used by:
# Subsystem: Loki Offensive - Projectile Scoping Array
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "power", src.getModifiedItemAttr("subsystemMPTFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "cpu", src.getModifiedItemAttr("subsystemMPTFittingReduction"))
