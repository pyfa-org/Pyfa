# ammoInfluenceRange
#
# Used by:
# Items from category: Charge (572 of 928)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))
