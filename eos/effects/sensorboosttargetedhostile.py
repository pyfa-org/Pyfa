# Used by:
# Drone: Hammerhead SD-600
# Drone: Hobgoblin SD-300
# Drone: Ogre SD-900
type = "projected", "active"
def handler(fit, container, context):
    if "projected" in context:
        fit.ship.multiplyItemAttr("maxTargetRange", container.getModifiedItemAttr("maxTargetRangeMultiplier"),
                                  stackingPenalties = True, penaltyGroup="postMul")
        fit.ship.multiplyItemAttr("scanResolution", container.getModifiedItemAttr("scanResolutionMultiplier"),
                                  stackingPenalties = True, penaltyGroup="postMul")
