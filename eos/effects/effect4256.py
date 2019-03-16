# subsystemBonusMinmatarOffensive2MissileLauncherROF
#
# Used by:
# Subsystem: Loki Offensive - Launcher Efficiency Configuration
type = "passive"


def handler(fit, src, context):
    groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "speed", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive2"),
                                  skill="Minmatar Offensive Systems")
