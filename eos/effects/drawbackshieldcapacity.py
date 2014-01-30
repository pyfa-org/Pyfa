# Used by:
# Modules from group: Rig Targeting (16 of 16)
# Modules named like: Diagnostic Subroutines (8 of 8)
# Modules named like: Dispersion (16 of 16)
# Modules named like: Inverted Signal Field Projector (8 of 8)
# Modules named like: Signal Focusing (8 of 8)
# Modules named like: Targeting Systems (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("shieldCapacity", module.getModifiedItemAttr("drawback"))
