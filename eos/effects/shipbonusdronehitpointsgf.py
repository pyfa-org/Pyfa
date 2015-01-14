# shipBonusDroneHitpointsGF
#
# Used by:
# Ships named like: Tristan (2 of 2)
# Ship: Astero
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    for layer in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     layer, ship.getModifiedItemAttr("shipBonusGF") * level)
