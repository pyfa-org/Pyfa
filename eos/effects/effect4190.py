# shipBonusStrategicCruiserMinmatarHeatDamage
#
# Used by:
# Ship: Loki
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserMinmatar1"),
                                  skill="Minmatar Strategic Cruiser")
