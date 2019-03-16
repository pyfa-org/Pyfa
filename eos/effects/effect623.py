# miningDroneOperationMiningAmountBonusPostPercentMiningDroneAmountPercentChar
#
# Used by:
# Modules named like: Drone Mining Augmentor (8 of 8)
# Skill: Mining Drone Operation
type = "passive"


def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                 "miningAmount",
                                 container.getModifiedItemAttr("miningAmountBonus") * level)
