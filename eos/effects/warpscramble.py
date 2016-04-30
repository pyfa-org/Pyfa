# warpScramble
#
# Used by:
# Variations of module: Heavy Warp Disruptor I (7 of 7)
# Variations of module: Warp Disruptor I (19 of 19)
# Module: Civilian Warp Disruptor
type = "projected", "active"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))