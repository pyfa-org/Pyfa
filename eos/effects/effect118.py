# electronicAttributeModifyOnline
#
# Used by:
# Modules from group: Automated Targeting System (6 of 6)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxLockedTargets", module.getModifiedItemAttr("maxLockedTargetsBonus"))
