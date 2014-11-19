# powerOutputMultiply
#
# Used by:
# Modules from group: Capacitor Flux Coil (6 of 6)
# Modules from group: Capacitor Power Relay (26 of 26)
# Modules from group: Power Diagnostic System (31 of 31)
# Modules from group: Reactor Control Unit (22 of 22)
# Modules from group: Shield Flux Coil (11 of 11)
# Modules from group: Shield Power Relay (11 of 11)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("powerOutput", module.getModifiedItemAttr("powerOutputMultiplier"))