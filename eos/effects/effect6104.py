# entosisDurationMultiply
#
# Used by:
# Items from market group: Ships > Capital Ships (31 of 40)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Infomorph Psychology"),
                                     "duration", ship.getModifiedItemAttr("entosisDurationMultiplier") or 1)
