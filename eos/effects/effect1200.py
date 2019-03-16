# miningInfoMultiplier
#
# Used by:
# Charges from group: Mining Crystal (40 of 40)
# Charges named like: Mining Crystal (42 of 42)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("specialtyMiningAmount",
                            module.getModifiedChargeAttr("specialisationAsteroidYieldMultiplier"))
    # module.multiplyItemAttr("miningAmount", module.getModifiedChargeAttr("specialisationAsteroidYieldMultiplier"))
