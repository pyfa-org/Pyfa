# Used by:
# Subsystems from group: Engineering Systems (13 of 16)
# Subsystems from group: Offensive Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("droneBandwidth", module.getModifiedItemAttr("droneBandwidth"))
