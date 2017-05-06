# ammoInfluenceRange
#
# Used by:
# Items from category: Charge (571 of 913)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))
