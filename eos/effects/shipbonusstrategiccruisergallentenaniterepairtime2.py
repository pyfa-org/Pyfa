# shipBonusStrategicCruiserGallenteNaniteRepairTime2
#
# Used by:
# Ship: Proteus
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserGallente2"),
                                  skill="Gallente Strategic Cruiser")
