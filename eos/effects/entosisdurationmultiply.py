# entosisDurationMultiply
#
# Used by:
# Ships from group: Carrier (4 of 4)
# Ships from group: Dreadnought (4 of 4)
# Ships from group: Supercarrier (5 of 5)
# Ships from group: Titan (4 of 4)
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.requiresSkill("Infomorph Psychology"),
                                     "duration", ship.getModifiedItemAttr("entosisDurationMultiplier") or 1)
