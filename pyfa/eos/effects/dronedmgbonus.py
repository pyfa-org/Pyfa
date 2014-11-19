# droneDmgBonus
#
# Used by:
# Skills from group: Drones (8 of 21)
# Skills named like: Drone Specialization (4 of 4)
type = "passive"
def handler(fit, skill, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill(skill),
                                 "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
