type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Navigation"), "maxRange", src.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
