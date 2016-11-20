# capacitorCapacityMultiply
#
# Used by:
# Modules from group: Capacitor Flux Coil (6 of 6)
# Modules from group: Capacitor Power Relay (20 of 20)
# Modules from group: Power Diagnostic System (23 of 23)
# Modules from group: Propulsion Module (65 of 127)
# Modules from group: Reactor Control Unit (22 of 22)
type = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("capacitorCapacity", module.getModifiedItemAttr("capacitorCapacityMultiplier"))
