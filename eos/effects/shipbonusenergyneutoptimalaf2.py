type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "maxRange", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")