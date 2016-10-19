# titanCaldariLeadershipModuleAmount4
#
# Used by:
# Ship: Leviathan
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator",
                                     "maxGroupActive", ship.getModifiedItemAttr("titanCaldariBonus4"),
                                     skill="Caldari Titan")
