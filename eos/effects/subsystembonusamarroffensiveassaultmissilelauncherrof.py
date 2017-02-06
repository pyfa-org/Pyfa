# subsystemBonusAmarrOffensiveAssaultMissileLauncherROF
#
# Used by:
# Subsystem: Legion Offensive - Assault Optimization
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Light",
                                  "speed", module.getModifiedItemAttr("subsystemBonusAmarrOffensive"),
                                  skill="Amarr Offensive Systems")
