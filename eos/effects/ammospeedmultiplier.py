# ammoSpeedMultiplier
#
# Used by:
# Charges from group: Festival Charges (9 of 9)
# Charges from group: Interdiction Probe (2 of 2)
# Charges from group: Survey Probe (3 of 3)
type = "passive"


def handler(fit, module, context):
    module.multiplyItemAttr("speed", module.getModifiedChargeAttr("speedMultiplier") or 1)
