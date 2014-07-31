# Used by:
# Skill: Drone Durability
type = "passive"
def handler(fit, skill, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "armorHP", skill.getModifiedItemAttr("armorHpBonus") * skill.level)