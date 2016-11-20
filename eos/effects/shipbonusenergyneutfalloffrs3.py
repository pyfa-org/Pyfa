# shipBonusEnergyNeutFalloffRS3
#
# Used by:
# Ship: Curse
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                  src.getModifiedItemAttr("eliteBonusReconShip3"), skill="Recon Ships")
