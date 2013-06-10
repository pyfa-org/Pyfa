# Used by:
# Modules named like: Processor Overclocking Unit II (4 of 4)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("shieldRechargeRate", module.getModifiedItemAttr("shieldRechargeRateMultiplier"))
