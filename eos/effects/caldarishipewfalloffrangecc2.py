# caldariShipEwFalloffRangeCC2
#
# Used by:
# Ship: Blackbird
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "falloff", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
