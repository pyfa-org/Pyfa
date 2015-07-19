# carrierMinmatarLeadershipMaxGroupActive4
#
# Used by:
# Ship: Hel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("carrierMinmatarBonus4"), skill="Minmatar Carrier")
