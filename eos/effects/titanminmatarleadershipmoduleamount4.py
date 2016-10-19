# titanMinmatarLeadershipModuleAmount4
#
# Used by:
# Ship: Ragnarok
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("titanMinmatarBonus4"),
                                     skill="Minmatar Titan")
