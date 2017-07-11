# subsystemBonusCaldariOffensive1LauncherROF
#
# Used by:
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
type = "passive"


def handler(fit, src, context):
    groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "speed", src.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
