# modifyShipAgilityPassivePreAssignment
#
# Used by:
# Subsystems from group: Propulsion Systems (12 of 12)
runTime = "early"
type = "passive"


def handler(fit, module, context):
    fit.ship.preAssignItemAttr("agility", module.getModifiedItemAttr("agility"))
