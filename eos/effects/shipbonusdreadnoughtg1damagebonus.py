type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusDreadnoughtG1"), skill="Gallente Dreadnought")
