# advancedDroneInterfacingMaxGroupDCUSkillLevel
#
# Used by:
# Skill: Advanced Drone Interfacing
type = "passive"
def handler(fit, skill, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Fighter Support Unit",
                                     "maxGroupActive", skill.level)
