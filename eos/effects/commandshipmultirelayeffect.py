# Used by:
# Ships from group: Command Ship (8 of 8)
# Ship: Orca
# Ship: Rorqual
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("maxGangModules"))
