# shipBonusDroneHitpointsFixedAC2
#
# Used by:
# Variations of ship: Arbitrator (3 of 3)
type = "passive"
def handler(fit, ship, context):
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     type, ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
