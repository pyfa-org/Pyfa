# overloadSelfDurationBonus
#
# Used by:
# Modules from group: Capacitor Booster (59 of 59)
# Modules from group: Energy Neutralizer (54 of 54)
# Modules from group: Energy Nosferatu (54 of 54)
# Modules from group: Hull Repair Unit (25 of 25)
# Modules from group: Remote Armor Repairer (39 of 39)
# Modules from group: Remote Capacitor Transmitter (41 of 41)
# Modules from group: Remote Shield Booster (38 of 38)
# Modules from group: Smart Bomb (118 of 118)
# Modules from group: Warp Disrupt Field Generator (7 of 7)
# Modules named like: Ancillary Remote (8 of 8)
# Module: Reactive Armor Hardener
# Module: Target Spectrum Breaker
type = "overheat"


def handler(fit, module, context):
    module.boostItemAttr("duration", module.getModifiedItemAttr("overloadSelfDurationBonus") or 0)
