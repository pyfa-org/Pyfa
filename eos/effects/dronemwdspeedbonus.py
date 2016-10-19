# droneMWDSpeedBonus
#
# Used by:
# Modules from group: Drone Navigation Computer (8 of 8)
type = "passive"


def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"), "maxVelocity",
                                 module.getModifiedItemAttr("speedFactor"), stackingPenalties=True)
