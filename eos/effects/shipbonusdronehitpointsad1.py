type = "passive"
def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity", src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp", src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP", src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
