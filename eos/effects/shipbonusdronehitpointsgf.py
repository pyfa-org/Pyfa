# shipBonusDroneHitpointsGF
#
# Used by:
# Ship: Astero
# Ship: Tristan
type = "passive"
def handler(fit, ship, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     layer, ship.getModifiedItemAttr("shipBonusGF"), skill="Gallente Frigate")
