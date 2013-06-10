# Used by:
# Modules from group: Drone Tracking Modules (7 of 7)
type = "passive"
def handler(fit, module, context):
    fit.drones.filteredItemMultiply(lambda drone: drone.item.requiresSkill("Drones"),
                                    "trackingSpeed", module.getModifiedItemAttr("trackingSpeedMultiplier"),
                                    stackingPenalties = True, penaltyGroup="postMul")
    fit.drones.filteredItemMultiply(lambda drone: drone.item.requiresSkill("Drones"),
                                    "maxRange", module.getModifiedItemAttr("maxRangeMultiplier"),
                                    stackingPenalties = True, penaltyGroup="postMul")
