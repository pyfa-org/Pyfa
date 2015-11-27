type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness", src.getModifiedItemAttr("shipBonus3AF"), skill="Amarr Frigate")
