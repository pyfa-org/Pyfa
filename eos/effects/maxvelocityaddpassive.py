# maxVelocityAddPassive
#
# Used by:
# Subsystems from group: Propulsion Systems (12 of 12)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocity"))
