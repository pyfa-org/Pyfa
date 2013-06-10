# Used by:
# Charge: Focused Warp Disruption Script
type = "passive"
runTime = "early"
def handler(fit, module, context):
    module.boostItemAttr("speedFactorBonus", module.getModifiedChargeAttr("speedFactorBonusBonus"))
