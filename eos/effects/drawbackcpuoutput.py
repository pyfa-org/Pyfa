# Used by:
# Modules from group: Rig Drones (64 of 64)
# Modules named like: Optimizer (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("cpuOutput", module.getModifiedItemAttr("drawback"))