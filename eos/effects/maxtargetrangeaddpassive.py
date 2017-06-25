# maxTargetRangeAddPassive
#
# Used by:
# Subsystems named like: Propulsion Interdiction Nullifier (4 of 4)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRange"))
