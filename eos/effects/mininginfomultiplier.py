# Used by:
# Charges from group: Mercoxit Mining Crystal (2 of 2)
# Charges from group: Mining Crystal (30 of 30)
type = "passive"
def handler(fit, module, context):
    module.multiplyItemAttr("miningAmount", module.getModifiedChargeAttr("specialisationAsteroidYieldMultiplier"))