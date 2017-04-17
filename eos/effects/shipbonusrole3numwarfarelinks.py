# shipBonusRole3NumWarfareLinks
#
# Used by:
# Ships from group: Force Auxiliary (5 of 5)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                     src.getModifiedItemAttr("shipBonusRole3"))
