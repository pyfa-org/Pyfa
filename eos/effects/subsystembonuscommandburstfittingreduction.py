# subsystemBonusCommandBurstFittingReduction
#
# Used by:
# Subsystems named like: Offensive Support Processor (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "power",
                                  src.getModifiedItemAttr("subsystemCommandBurstFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Leadership"), "cpu",
                                  src.getModifiedItemAttr("subsystemCommandBurstFittingReduction"))
