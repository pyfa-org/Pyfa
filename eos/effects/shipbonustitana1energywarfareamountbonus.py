type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "powerTransferAmount", src.getModifiedItemAttr("shipBonusTitanA1") * lvl, skill="Amarr Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "energyNeutralizerAmount", src.getModifiedItemAttr("shipBonusTitanA1") * lvl, skill="Amarr Titan")
