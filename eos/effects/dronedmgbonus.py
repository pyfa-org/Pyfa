# Used by:
# Skill: Amarr Drone Specialization
# Skill: Caldari Drone Specialization
# Skill: Gallente Drone Specialization
# Skill: Heavy Drone Operation
# Skill: Minmatar Drone Specialization
# Skill: Sentry Drone Interfacing
type = "passive"
def handler(fit, skill, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill(skill),
                                 "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
