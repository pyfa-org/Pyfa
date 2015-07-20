# shipBonusDroneTrackingGF
#
# Used by:
# Ship: Tristan
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "trackingSpeed", ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
