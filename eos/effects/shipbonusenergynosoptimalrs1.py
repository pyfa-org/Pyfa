type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange", src.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")
