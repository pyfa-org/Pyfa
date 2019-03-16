# shieldCapacityAddPassive
#
# Used by:
# Subsystems from group: Defensive Systems (8 of 12)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacity"))
