# Used by:
# Variations of module: Warp Scrambler I (19 of 19)
runTime = "early"
type = "projected", "active"
def handler(fit, module, context):
    if "projected" not in context:
        return

    fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))
