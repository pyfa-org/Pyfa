# Used by:
# Skills named like: Drone Specialization (4 of 4)
# Skill: Heavy Drone Operation
# Skill: Sentry Drone Interfacing
type = "passive"
def handler(fit, skill, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill(skill),
                                 "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
