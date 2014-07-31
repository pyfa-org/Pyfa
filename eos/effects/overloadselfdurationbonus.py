# Used by:
# Modules from group: Capacitor Booster (54 of 54)
# Modules from group: Energy Destabilizer (41 of 41)
# Modules from group: Energy Vampire (52 of 52)
# Modules from group: Hull Repair Unit (21 of 21)
# Modules from group: Remote Armor Repairer (38 of 38)
# Modules from group: Remote Capacitor Transmitter (38 of 38)
# Modules from group: Remote Shield Booster (39 of 39)
# Modules from group: Smart Bomb (118 of 118)
# Module: QA Remote Armor Repair System - 5 Players
# Module: QA Shield Transporter - 5 Players
# Module: Reactive Armor Hardener
# Module: Target Spectrum Breaker
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus") or 0)
