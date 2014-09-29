# warpSpeedAddition
#
# Used by:
# Modules from group: Warp Accelerator (3 of 3)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("warpSpeedMultiplier", module.getModifiedItemAttr("warpSpeedAdd"))
