# Used by:
# Skill: Cruise Missile Specialization
# Skill: Heavy Assault Missile Specialization
# Skill: Heavy Missile Specialization
# Skill: Light Missile Specialization
# Skill: Rocket Specialization
# Skill: Torpedo Specialization
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill(skill),
                                  "speed", skill.getModifiedItemAttr("rofBonus") * skill.level)