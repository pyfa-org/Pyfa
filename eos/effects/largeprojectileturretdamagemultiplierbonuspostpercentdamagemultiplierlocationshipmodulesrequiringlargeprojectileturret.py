# Used by:
# Implants named like: Eifyr and Co. 'Gunslinger' Large Projectile Turret LP (6 of 6)
# Skill: Large Projectile Turret
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Projectile Turret"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
