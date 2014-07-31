# Used by:
# Implants named like: Eifyr and Co. 'Gunslinger' Small Projectile Turret SP (6 of 6)
# Skill: Small Projectile Turret
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Projectile Turret"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
