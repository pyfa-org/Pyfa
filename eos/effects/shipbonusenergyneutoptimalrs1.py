type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "maxRange", ship.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")