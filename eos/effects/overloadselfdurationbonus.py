# overloadSelfDurationBonus
#
# Used by:
# Modules from group: Capacitor Booster (54 of 54)
# Modules from group: Energy Neutralizer (45 of 45)
# Modules from group: Energy Nosferatu (45 of 45)
# Modules from group: Hull Repair Unit (21 of 21)
# Modules from group: Remote Armor Repairer (33 of 33)
# Modules from group: Remote Capacitor Transmitter (38 of 38)
# Modules from group: Remote Shield Booster (31 of 31)
# Modules from group: Smart Bomb (118 of 118)
# Modules from group: Warp Disrupt Field Generator (7 of 7)
# Module: QA Remote Armor Repair System - 5 Players
# Module: QA Shield Transporter - 5 Players
# Module: Reactive Armor Hardener
# Module: Target Spectrum Breaker
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus") or 0)
