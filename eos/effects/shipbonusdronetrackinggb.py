# shipBonusDroneTrackingGB
#
# Used by:
# Ship: Dominix
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB"), skill="Gallente Battleship")
