# Used by:
# Drones named like: SD (3 of 3)
type = "projected", "active"
def handler(fit, container, context):
    if "projected" in context:
        fit.ship.multiplyItemAttr("maxTargetRange", container.getModifiedItemAttr("maxTargetRangeMultiplier"),
                                  stackingPenalties = True, penaltyGroup="postMul")
        fit.ship.multiplyItemAttr("scanResolution", container.getModifiedItemAttr("scanResolutionMultiplier"),
                                  stackingPenalties = True, penaltyGroup="postMul")
