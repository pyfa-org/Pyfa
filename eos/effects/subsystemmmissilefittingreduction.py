# subsystemMMissileFittingReduction
#
# Used by:
# Subsystem: Legion Offensive - Assault Optimization
# Subsystem: Loki Offensive - Launcher Efficiency Configuration
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
type = "passive"


def handler(fit, src, context):
    groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "cpu", src.getModifiedItemAttr("subsystemMMissileFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "power", src.getModifiedItemAttr("subsystemMMissileFittingReduction"))
