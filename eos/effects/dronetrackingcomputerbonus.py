# Used by:
# Variations of module: Omnidirectional Tracking Link I (7 of 7)
# Module: Sentient Omnidirectional Tracking Link
type = "active"
def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxRange", module.getModifiedItemAttr("maxRangeBonus"),
                                 stackingPenalties=True)
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "falloff", module.getModifiedItemAttr("falloffBonus"),
                                 stackingPenalties=True)
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                 stackingPenalties=True)

