# Used by:
# Subsystems from group: Engineering Systems (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("rechargeRate", module.getModifiedItemAttr("rechargeRate"))