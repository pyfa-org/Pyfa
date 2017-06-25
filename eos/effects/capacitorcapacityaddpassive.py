# capacitorCapacityAddPassive
#
# Used by:
# Subsystems from group: Defensive Systems (8 of 12)
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
# Subsystem: Proteus Offensive - Hybrid Encoding Platform
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("capacitorCapacity", module.getModifiedItemAttr("capacitorCapacity") or 0)
