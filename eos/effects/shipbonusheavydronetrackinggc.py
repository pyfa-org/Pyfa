# shipBonusHeavyDRoneTrackingGC
#
# Used by:
# Ship: Ishtar
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "trackingSpeed", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
