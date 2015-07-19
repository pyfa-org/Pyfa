# shipBonusDroneTrackingGC
#
# Used by:
# Ship: Vexor Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
