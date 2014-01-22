# Used by:
# Subsystems from group: Defensive Systems (16 of 16)
# Variations of subsystem: Loki Engineering - Power Core Multiplier (4 of 4)
# Variations of subsystem: Loki Offensive - Turret Concurrence Registry (4 of 4)
# Subsystem: Legion Engineering - Augmented Capacitor Reservoir
# Subsystem: Legion Engineering - Capacitor Regeneration Matrix
# Subsystem: Legion Engineering - Power Core Multiplier
# Subsystem: Legion Offensive - Assault Optimization
# Subsystem: Legion Offensive - Drone Synthesis Projector
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
# Subsystem: Proteus Engineering - Augmented Capacitor Reservoir
# Subsystem: Proteus Engineering - Capacitor Regeneration Matrix
# Subsystem: Proteus Engineering - Power Core Multiplier
# Subsystem: Proteus Offensive - Dissonic Encoding Platform
# Subsystem: Proteus Offensive - Drone Synthesis Projector
# Subsystem: Proteus Offensive - Hybrid Propulsion Armature
# Subsystem: Tengu Engineering - Augmented Capacitor Reservoir
# Subsystem: Tengu Engineering - Capacitor Regeneration Matrix
# Subsystem: Tengu Engineering - Power Core Multiplier
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
# Subsystem: Tengu Offensive - Rifling Launcher Pattern
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("droneCapacity", module.getModifiedItemAttr("droneCapacity"))
