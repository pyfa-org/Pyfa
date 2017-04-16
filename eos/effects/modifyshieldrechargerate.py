# modifyShieldRechargeRate
#
# Used by:
# Modules from group: Capacitor Power Relay (20 of 20)
# Modules from group: Power Diagnostic System (23 of 23)
# Modules from group: Reactor Control Unit (22 of 22)
# Modules from group: Shield Recharger (4 of 4)
# Modules named like: Flux Coil (12 of 12)
type = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("shieldRechargeRate", module.getModifiedItemAttr("shieldRechargeRateMultiplier") or 1)
