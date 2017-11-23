# subsystemBonusMinmatarOffensive2RemoteRepCapUse
#
# Used by:
# Subsystem: Loki Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") or mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "capacitorNeed", src.getModifiedItemAttr("subsystemBonusMinmatarOffensive2"),
                                  skill="Minmatar Offensive Systems")
