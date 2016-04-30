# droneMaxRangeBonus
#
# Used by:
# Modules named like: Drone Scope Chip (6 of 8)
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    stacking = False if "skill" in context else True
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxRange",
                                 container.getModifiedItemAttr("rangeSkillBonus") * level,
                                 stackingPenalties = stacking)
