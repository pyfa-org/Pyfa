# Used by:
# Implants named like: Zainou 'Deadeye' Large Hybrid Turret LH (6 of 6)
# Skill: Large Hybrid Turret
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
