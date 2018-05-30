# ammoInfluenceRange
#
# Used by:
# Items from category: Charge (587 of 947)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))
