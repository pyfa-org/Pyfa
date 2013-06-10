# Used by:
# Skills named like: Missile Specialization (4 of 4)
# Skill: Rocket Specialization
# Skill: Torpedo Specialization
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                  "speed", skill.getModifiedItemAttr("rofBonus") * skill.level)