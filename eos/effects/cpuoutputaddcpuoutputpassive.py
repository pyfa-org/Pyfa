# Used by:
# Subsystems from group: Electronic Systems (16 of 16)
# Subsystems named like: Defensive Adaptive (5 of 5)
# Subsystem: Legion Defensive - Augmented Plating
# Subsystem: Legion Defensive - Nanobot Injector
# Subsystem: Legion Offensive - Assault Optimization
# Subsystem: Legion Offensive - Drone Synthesis Projector
# Subsystem: Legion Offensive - Liquid Crystal Magnifiers
# Subsystem: Loki Defensive - Amplification Node
# Subsystem: Loki Offensive - Hardpoint Efficiency Configuration
# Subsystem: Loki Offensive - Projectile Scoping Array
# Subsystem: Loki Offensive - Turret Concurrence Registry
# Subsystem: Proteus Defensive - Augmented Plating
# Subsystem: Proteus Defensive - Nanobot Injector
# Subsystem: Proteus Offensive - Dissonic Encoding Platform
# Subsystem: Proteus Offensive - Drone Synthesis Projector
# Subsystem: Proteus Offensive - Hybrid Propulsion Armature
# Subsystem: Tengu Defensive - Amplification Node
# Subsystem: Tengu Defensive - Supplemental Screening
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
# Subsystem: Tengu Offensive - Rifling Launcher Pattern
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("cpuOutput", module.getModifiedItemAttr("cpuOutput"))
