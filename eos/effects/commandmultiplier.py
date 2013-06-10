# Used by:
# Skills named like: Warfare Specialist (4 of 5)
# Skill: Mining Director
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill(skill),
                                     "commandBonus", skill.level)
