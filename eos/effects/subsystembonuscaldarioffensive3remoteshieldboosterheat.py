# subsystemBonusCaldariOffensive3RemoteShieldBoosterHeat
#
# Used by:
# Subsystem: Tengu Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusCaldariOffensive3"),
                                  skill="Caldari Offensive Systems")
