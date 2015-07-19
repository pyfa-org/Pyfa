# subsystemBonusCaldariOffensiveAssaultMissileLauncherROF
#
# Used by:
# Variations of subsystem: Tengu Offensive - Accelerated Ejection Bay (3 of 4)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Light",
                                  "speed", module.getModifiedItemAttr("subsystemBonusCaldariOffensive"), skill="Caldari Offensive Systems")
