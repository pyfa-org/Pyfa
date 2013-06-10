# Used by:
# Modules from group: Rig Electronics Superiority (64 of 64)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldCapacity", module.getModifiedItemAttr("drawback"))
