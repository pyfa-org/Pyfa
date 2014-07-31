# Used by:
# Charge: Focused Warp Disruption Script
type = "passive"
def handler(fit, module, context):
    module.boostItemAttr("warpScrambleRange", module.getModifiedChargeAttr("warpScrambleRangeBonus"))
