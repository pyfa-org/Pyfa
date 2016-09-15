# entosisDurationMultiply
#
# Used by:
# Ships from group: Carrier (4 of 4)
# Ships from group: Dreadnought (5 of 5)
# Ships from group: Force Auxiliary (4 of 4)
# Ships from group: Supercarrier (6 of 6)
# Ships from group: Titan (5 of 5)
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Infomorph Psychology"),
                                     "duration", ship.getModifiedItemAttr("entosisDurationMultiplier") or 1)
