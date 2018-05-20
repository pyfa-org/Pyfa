# Not used by any item
type = "passive"


def handler(fit, skill, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", skill.getModifiedItemAttr("damageMultiplierBonus") * skill.level)
