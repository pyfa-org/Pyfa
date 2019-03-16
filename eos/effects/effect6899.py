# subsystemMRSBFittingReduction
#
# Used by:
# Subsystem: Loki Offensive - Support Processor
# Subsystem: Tengu Offensive - Support Processor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") and
                                              mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                  "cpu", src.getModifiedItemAttr("subsystemMRSBFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Shield Emission Systems") and
                                              mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                  "power", src.getModifiedItemAttr("subsystemMRSBFittingReduction"))
