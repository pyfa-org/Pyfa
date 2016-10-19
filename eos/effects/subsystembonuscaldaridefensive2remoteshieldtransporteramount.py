# subsystemBonusCaldariDefensive2RemoteShieldTransporterAmount
#
# Used by:
# Subsystem: Tengu Defensive - Adaptive Shielding
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "shieldBonus", module.getModifiedItemAttr("subsystemBonusCaldariDefensive2"),
                                  skill="Caldari Defensive Systems")
