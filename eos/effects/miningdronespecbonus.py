# miningDroneSpecBonus
#
# Used by:
# Skill: Mining Drone Specialization
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Drone Specialization"), "miningAmount",
                                 src.getModifiedItemAttr("miningAmountBonus") * lvl)
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Mining Drone Specialization"), "maxVelocity",
                                 src.getModifiedItemAttr("maxVelocityBonus") * lvl)
