# shipBonusStrategicCruiserGallenteHeatDamage
#
# Used by:
# Ship: Proteus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "heatDamage",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserGallente1"),
                                  skill="Gallente Strategic Cruiser")
