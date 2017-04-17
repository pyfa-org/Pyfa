type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1") * lvl, skill="Amarr Carrier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness", src.getModifiedItemAttr("shipBonusForceAuxiliaryA1") * lvl, skill="Amarr Carrier")
