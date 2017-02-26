# shipBonusDroneRepairMC1
#
# Used by:
# Ship: Rabisu
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldBonus",
                                 src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "structureDamageAmount",
                                 src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorDamageAmount",
                                 src.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
