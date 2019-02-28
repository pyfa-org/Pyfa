# skillBonusDroneDurabilityNotFighters
#
# Used by:
# Implants from group: Cyber Drones (4 of 4)
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp",
                                 src.getModifiedItemAttr("hullHpBonus"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP",
                                 src.getModifiedItemAttr("armorHpBonus"))
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity",
                                 src.getModifiedItemAttr("shieldCapacityBonus"))
