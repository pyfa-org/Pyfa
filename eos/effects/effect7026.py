# scriptStandupWarpScram
#
# Used by:
# Charge: Standup Focused Warp Scrambling Script

type = "passive"
runTime = "early"


def handler(fit, src, context, *args, **kwargs):
    src.boostItemAttr("maxRange", src.getModifiedChargeAttr("warpScrambleRangeBonus"))
