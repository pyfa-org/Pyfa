# Used by:
# Module: Capital Processor Overclocking Unit II
# Module: Large Processor Overclocking Unit II
# Module: Medium Processor Overclocking Unit II
# Module: Small Processor Overclocking Unit II
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("shieldRechargeRate", module.getModifiedItemAttr("shieldRechargeRateMultiplier"))
