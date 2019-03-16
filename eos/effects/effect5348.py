# shipBonusDroneHitpointsGBC1
#
# Used by:
# Variations of ship: Myrmidon (2 of 2)
type = "passive"


def handler(fit, ship, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     layer, ship.getModifiedItemAttr("shipBonusGBC1"), skill="Gallente Battlecruiser")
