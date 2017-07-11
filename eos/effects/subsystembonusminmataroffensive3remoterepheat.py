# subsystemBonusMinmatarOffensive3RemoteRepHeat
#
# Used by:
# Subsystem: Loki Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "overloadSelfDurationBonus", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive3"),
                                  skill="Minmatar Offensive Systems")
