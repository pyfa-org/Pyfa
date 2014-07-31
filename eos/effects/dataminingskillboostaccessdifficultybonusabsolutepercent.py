# Used by:
# Skill: Archaeology
# Skill: Hacking
# Skill: Salvaging
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill(skill), "accessDifficultyBonus",
                                     skill.getModifiedItemAttr("accessDifficultyBonusAbsolutePercent") * skill.level)
