# shipBonusDroneHitpointsGD1
#
# Used by:
# Variations of ship: Algos (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                 src.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                 src.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                 src.getModifiedItemAttr("shipBonusGD1"), skill="Gallente Destroyer")
