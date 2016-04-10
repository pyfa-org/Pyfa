type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.drones.filteredItemBoost(lambda mod: mod.item.requiresSkill("Drones"), "maxVelocity", src.getModifiedItemAttr("droneMaxVelocityBonus") * lvl)
    fit.fighters.filteredItemBoost(lambda mod: mod.item.requiresSkill("Fighters"), "maxVelocity", src.getModifiedItemAttr("droneMaxVelocityBonus") * lvl)
