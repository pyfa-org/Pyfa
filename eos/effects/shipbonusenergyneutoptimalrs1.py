# shipBonusEnergyNeutOptimalRS1
#
# Used by:
# Ship: Curse
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                  src.getModifiedItemAttr("eliteBonusReconShip1"), skill="Recon Ships")
