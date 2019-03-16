# warfareLinkCpuPenalty
#
# Used by:
# Subsystems from group: Offensive Systems (8 of 12)
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"),
                                     "warfareLinkCPUAdd", module.getModifiedItemAttr("warfareLinkCPUPenalty"))
