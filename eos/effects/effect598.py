# ammoSpeedMultiplier
#
# Used by:
# Charges from group: Festival Charges (26 of 26)
# Charges from group: Interdiction Probe (2 of 2)
# Items from market group: Special Edition Assets > Special Edition Festival Assets (30 of 33)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("speed", module.getModifiedChargeAttr("speedMultiplier") or 1)
