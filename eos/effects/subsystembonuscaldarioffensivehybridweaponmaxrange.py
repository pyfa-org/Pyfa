# Used by:
# Subsystem: Tengu Offensive - Magnetic Infusion Basin
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Offensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"),
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusCaldariOffensive") * level)
