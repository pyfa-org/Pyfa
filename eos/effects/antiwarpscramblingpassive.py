# Used by:
# Modules from group: Warp Core Stabilizer (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("warmScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))