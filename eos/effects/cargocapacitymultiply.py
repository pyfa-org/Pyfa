# cargoCapacityMultiply
#
# Used by:
# Modules from group: Expanded Cargohold (7 of 7)
# Modules from group: Overdrive Injector System (7 of 7)
# Modules from group: Reinforced Bulkhead (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("capacity", module.getModifiedItemAttr("cargoCapacityMultiplier"))
