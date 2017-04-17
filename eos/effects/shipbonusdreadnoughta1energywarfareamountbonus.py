type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "powerTransferAmount", src.getModifiedItemAttr("shipBonusDreadnoughtA1") * lvl, skill="Amarr Dreadnought")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "energyNeutralizerAmount", src.getModifiedItemAttr("shipBonusDreadnoughtA1") * lvl, skill="Amarr Dreadnought")
