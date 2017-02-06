# shipBonusDroneOptimalRangeGB
#
# Used by:
# Ship: Dominix
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxRange", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")
