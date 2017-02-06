# modifyPowerRechargeRate
#
# Used by:
# Modules from group: Capacitor Flux Coil (6 of 6)
# Modules from group: Capacitor Power Relay (20 of 20)
# Modules from group: Capacitor Recharger (18 of 18)
# Modules from group: Power Diagnostic System (23 of 23)
# Modules from group: Reactor Control Unit (22 of 22)
# Modules from group: Shield Power Relay (6 of 6)
type = "passive"


def handler(fit, module, context):
    fit.ship.multiplyItemAttr("rechargeRate", module.getModifiedItemAttr("capacitorRechargeRateMultiplier"))
