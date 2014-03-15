# Used by:
# Variations of subsystem: Tengu Offensive - Accelerated Ejection Bay (3 of 4)
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                  "speed", module.getModifiedItemAttr("subsystemBonusCaldariOffensive") * level)
