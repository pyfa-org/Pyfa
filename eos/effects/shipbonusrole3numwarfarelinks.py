# shipBonusForceAuxiliaryRole3NumWarfareLinks
#
# Used by:
# Ships from group: Force Auxiliary (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.requiresSkill("Leadership"), "maxGroupActive",
                                     src.getModifiedItemAttr("shipBonusRole3"))
