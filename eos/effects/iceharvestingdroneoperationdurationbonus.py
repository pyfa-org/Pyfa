# iceHarvestingDroneOperationDurationBonus
#
# Used by:
# Modules named like: Drone Mining Augmentor (8 of 8)
# Skill: Ice Harvesting Drone Operation
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Ice Harvesting Drone Operation"), "duration", src.getModifiedItemAttr("rofBonus"))
