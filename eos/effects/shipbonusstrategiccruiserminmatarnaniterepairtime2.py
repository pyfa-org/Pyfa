# shipBonusStrategicCruiserMinmatarNaniteRepairTime2
#
# Used by:
# Ship: Loki
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserMinmatar2"),
                                  skill="Minmatar Strategic Cruiser")
