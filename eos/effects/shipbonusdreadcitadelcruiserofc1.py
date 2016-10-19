# shipBonusDreadCitadelCruiseRofC1
#
# Used by:
# Ship: Phoenix
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("XL Cruise Missiles"),
                                  "speed", ship.getModifiedItemAttr("dreadnoughtShipBonusC1"),
                                  skill="Caldari Dreadnought")
