# subsystemBonusCaldariDefensive3ShieldBoostHeat
#
# Used by:
# Subsystem: Tengu Defensive - Amplification Node
# Subsystem: Tengu Defensive - Covert Reconfiguration
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "overloadShieldBonus", src.getModifiedItemAttr("subsystemBonusCaldariDefensive3"),
                                  skill="Caldari Defensive Systems")
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Operation"),
                                  "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusCaldariDefensive3"),
                                  skill="Caldari Defensive Systems")
