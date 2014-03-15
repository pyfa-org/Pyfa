# Used by:
# Drones named like: TD (3 of 3)
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
