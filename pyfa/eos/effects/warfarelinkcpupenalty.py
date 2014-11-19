# warfareLinkCpuPenalty
#
# Used by:
# Subsystems from group: Defensive Systems (12 of 16)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"),
                                     "warfareLinkCPUAdd", module.getModifiedItemAttr("warfareLinkCPUPenalty"))

