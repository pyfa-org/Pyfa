# Used by:
# Drone: Acolyte TD-300
# Drone: Infiltrator TD-600
# Drone: Praetor TD-900
type = "projected", "active"
def handler(fit, container, context):
    if "projected" in context:
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                         "trackingSpeed", container.getModifiedItemAttr("trackingSpeedMultiplier"),
                                         stackingPenalties = True, penaltyGroup="postMul")
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                         "maxRange", container.getModifiedItemAttr("maxRangeMultiplier"),
                                         stackingPenalties = True, penaltyGroup="postMul")
        fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Gunnery"),
                                         "falloff", container.getModifiedItemAttr("fallofMultiplier"),
                                         stackingPenalties = True, penaltyGroup="postMul")
