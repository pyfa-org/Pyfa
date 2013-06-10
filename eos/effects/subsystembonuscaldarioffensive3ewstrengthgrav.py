# Used by:
# Subsystem: Tengu Offensive - Rifling Launcher Pattern
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "scanGravimetricStrengthBonus", module.getModifiedItemAttr("subsystemBonusCaldariOffensive3") * level)
