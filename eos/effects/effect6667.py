# skillBonusDroneNavigation
#
# Used by:
# Skill: Drone Navigation
type = "passive"


def handler(fit, src, context):
    lvl = src.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity",
                                 src.getModifiedItemAttr("maxVelocityBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity",
                                   src.getModifiedItemAttr("maxVelocityBonus") * lvl)
