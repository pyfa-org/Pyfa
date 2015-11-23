type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "falloffEffectiveness", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")