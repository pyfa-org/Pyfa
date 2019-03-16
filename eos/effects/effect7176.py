# skillBonusDroneInterfacingNotFighters
#
# Used by:
# Implant: CreoDron 'Bumblebee' Drone Tuner T10-5D
# Implant: CreoDron 'Yellowjacket' Drone Tuner D5-10T
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier",
                                 src.getModifiedItemAttr("damageMultiplierBonus"))
