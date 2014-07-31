# Used by:
# Implants named like: Eifyr and Co. 'Gunslinger' Medium Projectile Turret MP (6 of 6)
# Skill: Medium Projectile Turret
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Projectile Turret"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
