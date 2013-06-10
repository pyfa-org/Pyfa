# Used by:
# Skill: Information Warfare Specialist
runTime = "early"
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill(skill),
                                     "commandBonusHidden", skill.level)
