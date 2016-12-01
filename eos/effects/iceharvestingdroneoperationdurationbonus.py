# iceHarvestingDroneOperationDurationBonus
#
# Used by:
# Modules named like: Drone Mining Augmentor (8 of 8)
# Skill: Ice Harvesting Drone Operation
type = "passive"
def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Ice Harvesting Drone Operation"), "duration", src.getModifiedItemAttr("rofBonus"))
