type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusElectronicAttackShip1"), skill="Electronic Attack Ships")