# shipBonusEnergyNosFalloffEAF3
#
# Used by:
# Ship: Sentinel
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                  src.getModifiedItemAttr("eliteBonusElectronicAttackShip3"),
                                  skill="Electronic Attack Ships")
