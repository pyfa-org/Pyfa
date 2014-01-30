# Used by:
# Subsystems from group: Offensive Systems (16 of 16)
# Variations of subsystem: Loki Engineering - Power Core Multiplier (4 of 4)
# Subsystem: Legion Engineering - Augmented Capacitor Reservoir
# Subsystem: Legion Engineering - Capacitor Regeneration Matrix
# Subsystem: Legion Engineering - Power Core Multiplier
# Subsystem: Proteus Engineering - Augmented Capacitor Reservoir
# Subsystem: Proteus Engineering - Capacitor Regeneration Matrix
# Subsystem: Proteus Engineering - Power Core Multiplier
# Subsystem: Tengu Engineering - Augmented Capacitor Reservoir
# Subsystem: Tengu Engineering - Capacitor Regeneration Matrix
# Subsystem: Tengu Engineering - Power Core Multiplier
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("droneBandwidth", module.getModifiedItemAttr("droneBandwidth"))
