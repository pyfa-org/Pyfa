# moduleBonusCapitalDroneDurabilityEnhancer
#
# Used by:
# Variations of module: Capital Drone Durability Enhancer I (2 of 2)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                 src.getModifiedItemAttr("hullHpBonus"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                 src.getModifiedItemAttr("hullHpBonus"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                 src.getModifiedItemAttr("hullHpBonus"))
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "shieldCapacity",
                                   src.getModifiedItemAttr("hullHpBonus"))
    fit.ship.boostItemAttr("cpuOutput", src.getModifiedItemAttr("drawback"))
