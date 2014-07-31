# Used by:
# Modules from group: Rig Electronic Systems (40 of 48)
# Modules from group: Rig Targeting (16 of 16)
# Modules named like: Signal Focusing Kit (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldCapacity", module.getModifiedItemAttr("drawback"))
