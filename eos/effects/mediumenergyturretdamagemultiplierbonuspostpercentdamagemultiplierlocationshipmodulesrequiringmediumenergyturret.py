# Used by:
# Implants named like: Inherent Implants 'Lancer' Medium Energy Turret ME (6 of 6)
# Skill: Medium Energy Turret
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Energy Turret"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
