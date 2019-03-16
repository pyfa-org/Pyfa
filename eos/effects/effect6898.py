# subsystemMRARFittingReduction
#
# Used by:
# Subsystems named like: Offensive Support Processor (3 of 4)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") and
                                              mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                  "cpu", src.getModifiedItemAttr("subsystemMRARFittingReduction"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems") and
                                              mod.getModifiedItemAttr('mediumRemoteRepFittingMultiplier', 0) == 1,
                                  "power", src.getModifiedItemAttr("subsystemMRARFittingReduction"))
