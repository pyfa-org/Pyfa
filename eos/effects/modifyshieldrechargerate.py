# Used by:
# Modules from group: Capacitor Flux Coil (12 of 12)
# Modules from group: Capacitor Power Relay (26 of 26)
# Modules from group: Power Diagnostic System (31 of 31)
# Modules from group: Reactor Control Unit (28 of 28)
# Modules from group: Shield Flux Coil (11 of 11)
# Modules from group: Shield Recharger (6 of 6)
# Module: QA Multiship Module - 10 Players
# Module: QA Multiship Module - 20 Players
# Module: QA Multiship Module - 40 Players
# Module: QA Multiship Module - 5 Players
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("shieldRechargeRate", module.getModifiedItemAttr("shieldRechargeRateMultiplier") or 1)
