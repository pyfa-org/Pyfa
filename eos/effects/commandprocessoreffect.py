# commandProcessorEffect
#
# Used by:
# Modules named like: Command Processor I (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                     src.getModifiedItemAttr("maxGangModules"))
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupOnline",
                                     src.getModifiedItemAttr("maxGangModules"))
