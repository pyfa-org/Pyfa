# Used by:
# Items from category: Subsystem (42 of 80)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("droneCapacity", module.getModifiedItemAttr("droneCapacity"))
