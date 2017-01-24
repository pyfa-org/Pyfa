# commandshipMultiRelayEffect
#
# Used by:
# Ships from group: Command Ship (8 of 8)
# Ships from group: Industrial Command Ship (2 of 2)
# Ship: Rorqual
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                     src.getModifiedItemAttr("maxGangModules"))
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupOnline",
                                     src.getModifiedItemAttr("maxGangModules"))
