# droneTrackingEnhancerBonus
#
# Used by:
# Modules from group: Drone Tracking Enhancer (9 of 9)
type = "passive"
def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                 stackingPenalties = True)
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "falloff", module.getModifiedItemAttr("falloffBonus"),
                                 stackingPenalties = True)
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                 stackingPenalties = True)
