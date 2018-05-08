# shieldCapacityMultiply
#
# Used by:
# Modules from group: Capacitor Power Relay (20 of 20)
# Modules from group: Power Diagnostic System (23 of 23)
# Modules from group: Reactor Control Unit (22 of 22)
# Modules named like: Flux Coil (12 of 12)
type = "passive"


def handler(fit, module, context):
    # We default this to None as there are times when the source attribute doesn't exist (for example, Cap Power Relay).
    # It will return 0 as it doesn't exist, which would nullify whatever the target attribute is
    fit.ship.multiplyItemAttr("shieldCapacity", module.getModifiedItemAttr("shieldCapacityMultiplier", None))
