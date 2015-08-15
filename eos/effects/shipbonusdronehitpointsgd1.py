# shipBonusDroneHitpointsGD1
#
# Used by:
# Ship: Algos
type = "passive"
def handler(fit, ship, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     layer, ship.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
