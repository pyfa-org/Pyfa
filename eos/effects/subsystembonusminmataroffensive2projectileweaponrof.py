# Used by:
# Subsystem: Loki Offensive - Hardpoint Efficiency Configuration
# Subsystem: Loki Offensive - Projectile Scoping Array
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "speed", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive2") * level)
