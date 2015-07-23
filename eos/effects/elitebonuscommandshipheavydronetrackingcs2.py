# eliteBonusCommandShipHeavyDroneTrackingCS2
#
# Used by:
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "trackingSpeed", ship.getModifiedItemAttr("eliteBonusCommandShips2"), skill="Command Ships")
