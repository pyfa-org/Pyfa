# droneCapacityAdddroneCapacityPassive
#
# Used by:
# Subsystems from group: Offensive Systems (12 of 12)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("droneCapacity", module.getModifiedItemAttr("droneCapacity"))
