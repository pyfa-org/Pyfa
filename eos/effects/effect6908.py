# shipBonusStrategicCruiserCaldariNaniteRepairTime2
#
# Used by:
# Ship: Tengu
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: True, "moduleRepairRate",
                                  ship.getModifiedItemAttr("shipBonusStrategicCruiserCaldari2"),
                                  skill="Caldari Strategic Cruiser")
