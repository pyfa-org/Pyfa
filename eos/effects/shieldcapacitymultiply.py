# shieldCapacityMultiply
#
# Used by:
# Modules from group: Capacitor Flux Coil (6 of 6)
# Modules from group: Capacitor Power Relay (20 of 20)
# Modules from group: Power Diagnostic System (23 of 23)
# Modules from group: Reactor Control Unit (22 of 22)
# Modules from group: Shield Flux Coil (11 of 11)
# Modules from group: Shield Power Relay (11 of 11)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacityMultiplier"))