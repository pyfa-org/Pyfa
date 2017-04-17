type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange", src.getModifiedItemAttr("shipBonusDreadnoughtM1") * lvl, skill="Minmatar Dreadnought")
