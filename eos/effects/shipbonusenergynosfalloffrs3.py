type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "falloffEffectiveness", ship.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")