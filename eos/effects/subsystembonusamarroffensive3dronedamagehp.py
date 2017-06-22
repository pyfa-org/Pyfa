type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "hp", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3") * lvl, skill="Amarr Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "armorHP", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3") * lvl, skill="Amarr Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "shieldCapacity", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3") * lvl, skill="Amarr Offensive Systems")
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "damageMultiplier", src.getModifiedItemAttr("subsystemBonusAmarrOffensive3") * lvl, skill="Amarr Offensive Systems")
