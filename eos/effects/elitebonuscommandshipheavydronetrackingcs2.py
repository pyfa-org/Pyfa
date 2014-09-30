# eliteBonusCommandShipHeavyDroneTrackingCS2
#
# Used by:
# Ship: Eos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "trackingSpeed", ship.getModifiedItemAttr("eliteBonusCommandShips2") * level)
