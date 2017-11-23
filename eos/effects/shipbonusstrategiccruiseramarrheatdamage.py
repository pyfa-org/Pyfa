# shipBonusStrategicCruiserAmarrHeatDamage
#
# Used by:
# Ship: Legion
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserAmarr1"),
                                  skill="Amarr Strategic Cruiser")
