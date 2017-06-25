# Not used by any item
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"),
                                     "warfareLinkCPUAdd", module.getModifiedItemAttr("warfareLinkCPUPenalty"))
