# shipBonusDroneHitpointsGD1
#
# Used by:
# Ship: Algos
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Destroyer").level
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     layer, ship.getModifiedItemAttr("shipBonusGD1") * level)
