# Used by:
# Modules from group: Capacitor Flux Coil (12 of 12)
# Modules from group: Capacitor Power Relay (25 of 25)
# Modules from group: Power Diagnostic System (31 of 31)
# Modules from group: Reactor Control Unit (28 of 28)
# Modules from group: Shield Flux Coil (11 of 11)
# Modules from group: Shield Power Relay (11 of 11)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacityMultiplier"))