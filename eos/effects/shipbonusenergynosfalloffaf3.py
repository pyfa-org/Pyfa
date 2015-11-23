type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "falloffEffectiveness", ship.getModifiedItemAttr("shipBonus3AF"), skill="Amarr Frigate")