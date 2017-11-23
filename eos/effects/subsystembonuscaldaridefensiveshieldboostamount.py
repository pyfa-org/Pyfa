# subsystemBonusCaldariDefensiveShieldBoostAmount
#
# Used by:
# Subsystem: Tengu Defensive - Amplification Node
# Subsystem: Tengu Defensive - Covert Reconfiguration
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "shieldBonus", module.getModifiedItemAttr("subsystemBonusCaldariDefensive"),
                                  skill="Caldari Defensive Systems")
