# largeDisintegratorSkillDmgBonus
#
# Used by:
# Skill: Large Disintegrator Specialization
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Disintegrator Specialization"),
                                  "damageMultiplier", container.getModifiedItemAttr("damageMultiplierBonus") * level)
