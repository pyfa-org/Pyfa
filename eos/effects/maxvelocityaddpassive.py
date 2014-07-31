# Used by:
# Subsystems from group: Propulsion Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocity"))