# ammoInfluenceRange
#
# Used by:
# Items from category: Charge (587 of 943)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))
