# titanGallenteLeadershipModuleAmount4
#
# Used by:
# Ship: Erebus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("titanGallenteBonus4"),
                                     skill="Gallente Titan")
