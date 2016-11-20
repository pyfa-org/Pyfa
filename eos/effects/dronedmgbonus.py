# droneDmgBonus
#
# Used by:
# Skills from group: Drones (8 of 26)
type = "passive"


def handler(fit, skill, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill(skill),
                                 "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
