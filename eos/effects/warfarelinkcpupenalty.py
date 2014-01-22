# Used by:
# Subsystems named like: Adaptive (5 of 5)
# Subsystem: Legion Defensive - Augmented Plating
# Subsystem: Legion Defensive - Nanobot Injector
# Subsystem: Loki Defensive - Amplification Node
# Subsystem: Proteus Defensive - Augmented Plating
# Subsystem: Proteus Defensive - Nanobot Injector
# Subsystem: Tengu Defensive - Amplification Node
# Subsystem: Tengu Defensive - Supplemental Screening
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"),
                                     "warfareLinkCPUAdd", module.getModifiedItemAttr("warfareLinkCPUPenalty"))

