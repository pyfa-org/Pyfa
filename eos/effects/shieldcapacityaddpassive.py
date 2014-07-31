# Used by:
# Subsystems from group: Defensive Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacity"))
