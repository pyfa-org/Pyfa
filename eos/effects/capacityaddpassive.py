# capacityAddPassive
#
# Used by:
# Subsystems named like: Defensive Covert Reconfiguration (4 of 4)
# Subsystem: Legion Defensive - Nanobot Injector
type = "passive"


def handler(fit, subsystem, context):
    fit.ship.increaseItemAttr("capacity", subsystem.getModifiedItemAttr("cargoCapacityAdd") or 0)
