# shipBonusDroneHitpointsGC2
#
# Used by:
# Ships named like: Stratios (2 of 2)
# Ship: Vexor
# Ship: Vexor Navy Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Cruiser").level
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     type, ship.getModifiedItemAttr("shipBonusGC2") * level)
