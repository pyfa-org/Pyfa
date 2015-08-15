# carrierAmarrLeadershipMaxGroupActive4
#
# Used by:
# Ship: Aeon
# Ship: Revenant
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("carrierAmarrBonus4"), skill="Amarr Carrier")
