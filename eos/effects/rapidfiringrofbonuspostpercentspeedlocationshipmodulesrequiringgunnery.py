# Used by:
# Skill: Rapid Firing
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Gunnery"),
                                  "speed", skill.getModifiedItemAttr("rofBonus") * skill.level)