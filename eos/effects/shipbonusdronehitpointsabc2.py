# shipBonusDroneHitpointsABC2
#
# Used by:
# Ship: Prophecy
type = "passive"
def handler(fit, ship, context):
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     layer, ship.getModifiedItemAttr("shipBonusABC2"), skill="Amarr Battlecruiser")
