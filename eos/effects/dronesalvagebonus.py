# Used by:
# Skill: Salvage Drone Operation
type = "passive"
def handler(fit, container, context):
    fit.drones.filteredItemIncrease(lambda drone: drone.item.requiresSkill("Salvage Drone Operation"),
                                    "accessDifficultyBonus", container.getModifiedItemAttr("accessDifficultyBonus") * container.level)
