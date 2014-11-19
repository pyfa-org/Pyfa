# shipBonusHeavyDroneSpeedGC
#
# Used by:
# Ship: Ishtar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Heavy Drone Operation"),
                                 "maxVelocity", ship.getModifiedItemAttr("shipBonusGC") * level)
