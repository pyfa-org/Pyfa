# carrierGallenteLeadershipMaxGroupActive4
#
# Used by:
# Ship: Nyx
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("carrierGallenteBonus4"), skill="Gallente Carrier")
