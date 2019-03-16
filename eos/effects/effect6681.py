# shipBonusRole3NumWarfareLinks
#
# Used by:
# Ships from group: Force Auxiliary (6 of 6)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                     src.getModifiedItemAttr("shipBonusRole3"))
