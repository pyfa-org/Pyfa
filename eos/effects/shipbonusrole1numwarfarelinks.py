# shipBonusRole1NumWarfareLinks
#
# Used by:
# Ships from group: Titan (7 of 7)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                     src.getModifiedItemAttr("shipBonusRole1"))
