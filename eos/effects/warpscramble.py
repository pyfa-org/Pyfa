# warpScramble
#
# Used by:
# Modules named like: Warp Disruptor (27 of 27)
type = "projected", "active"


def handler(fit, module, context):
    if "projected" in context:
        fit.ship.increaseItemAttr("warpScrambleStatus", module.getModifiedItemAttr("warpScrambleStrength"))
