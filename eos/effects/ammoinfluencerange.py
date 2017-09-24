# ammoInfluenceRange
#
# Used by:
# Items from category: Charge (568 of 910)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))
