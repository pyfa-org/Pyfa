# Used by:
# Subsystem: Loki Offensive - Turret Concurrence Registry
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusMinmatarOffensive") * level)
