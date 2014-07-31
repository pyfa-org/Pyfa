# Used by:
# Subsystems from group: Engineering Systems (16 of 16)
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("capacitorCapacity",
                              module.getModifiedItemAttr("capacitorCapacity"))
