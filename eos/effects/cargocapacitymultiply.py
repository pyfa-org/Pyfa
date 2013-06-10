# Used by:
# Modules from group: Expanded Cargohold (13 of 13)
# Modules from group: Overdrive Injector System (14 of 14)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("capacity", module.getModifiedItemAttr("cargoCapacityMultiplier"))
