# Used by:
# Subsystems from group: Defensive Systems (16 of 16)
type = "passive"
def handler(fit, subsystem, context):
    fit.ship.increaseItemAttr("capacity", subsystem.getModifiedItemAttr("capacity") or 0)
