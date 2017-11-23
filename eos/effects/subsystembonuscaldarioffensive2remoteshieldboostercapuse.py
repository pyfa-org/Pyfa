# subsystemBonusCaldariOffensive2RemoteShieldBoosterCapUse
#
# Used by:
# Subsystem: Tengu Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems"),
                                  "capacitorNeed", src.getModifiedItemAttr("subsystemBonusCaldariOffensive2"),
                                  skill="Caldari Offensive Systems")
