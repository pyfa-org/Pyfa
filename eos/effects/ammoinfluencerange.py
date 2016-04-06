# ammoInfluenceRange
#
# Used by:
# Items from category: Charge (571 of 885)
type = "passive"
def handler(fit, module, context):
    module.multiplyItemAttr("maxRange", module.getModifiedChargeAttr("weaponRangeMultiplier"))