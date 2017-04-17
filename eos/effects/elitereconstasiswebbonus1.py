type = "passive"
def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange", src.getModifiedItemAttr("eliteBonusReconShip1") * lvl, skill="Recon Ships")
