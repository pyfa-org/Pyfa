# shipBonusEnergyNeutFalloffRS2
#
# Used by:
# Ship: Pilgrim
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                  src.getModifiedItemAttr("eliteBonusReconShip2"), skill="Recon Ships")
