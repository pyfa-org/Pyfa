# iceHarvestingDroneSpecBonus
#
# Used by:
# Skill: Ice Harvesting Drone Specialization
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Specialization"), "duration",
                                 src.getModifiedItemAttr("rofBonus") * lvl)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Specialization"),
                                 "maxVelocity", src.getModifiedItemAttr("maxVelocityBonus") * lvl)
