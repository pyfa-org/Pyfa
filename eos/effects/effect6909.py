# shipBonusStrategicCruiserAmarrNaniteRepairTime2
#
# Used by:
# Ship: Legion
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserAmarr2"),
                                  skill="Amarr Strategic Cruiser")
