# entosisDurationMultiply
#
# Used by:
# Ships from group: Supercarrier (5 of 5)
# Items from market group: Ships > Capital Ships (22 of 32)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Infomorph Psychology"),
                                     "duration", ship.getModifiedItemAttr("entosisDurationMultiplier") or 1)
