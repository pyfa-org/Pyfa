# Used by:
# Subsystem: Tengu Defensive - Amplification Node
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Defensive Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", module.getModifiedItemAttr("subsystemBonusCaldariDefensive") * level)
