# shipBonusEnergyNeutOptimalEAF1
#
# Used by:
# Ship: Sentinel
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                  src.getModifiedItemAttr("eliteBonusElectronicAttackShip1"),
                                  skill="Electronic Attack Ships")
