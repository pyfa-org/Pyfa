# Used by:
# Subsystems from group: Electronic Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRange"))