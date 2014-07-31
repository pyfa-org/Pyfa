# Used by:
# Modules from group: Warp Core Stabilizer (8 of 8)
# Module: Target Spectrum Breaker
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionMultiplier"),
                              stackingPenalties = True)