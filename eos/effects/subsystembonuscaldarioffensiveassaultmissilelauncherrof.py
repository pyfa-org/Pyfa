# Used by:
# Subsystem: Tengu Offensive - Accelerated Ejection Bay
# Subsystem: Tengu Offensive - Covert Reconfiguration
# Subsystem: Tengu Offensive - Rifling Launcher Pattern
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Light",
                                  "speed", module.getModifiedItemAttr("subsystemBonusCaldariOffensive") * level)
