# shipBonusDroneHitpointsAD1
#
# Used by:
# Ship: Dragoon
type = "passive"
def handler(fit, ship, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     layer, ship.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
