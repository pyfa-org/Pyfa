# subsystemBonusAmarrOffensiveMissileLauncherROF
#
# Used by:
# Subsystem: Legion Offensive - Assault Optimization
type = "passive"


def handler(fit, src, context):
    groups = ("Missile Launcher Heavy", "Missile Launcher Rapid Light", "Missile Launcher Heavy Assault")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "speed", src.getModifiedItemAttr("subsystemBonusAmarrOffensive"), skill="Amarr Offensive Systems")
