type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "powerTransferAmount", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1") * lvl, skill="Amarr Carrier")
