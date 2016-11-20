# shipBonusEnergyNeutFalloffAD1
#
# Used by:
# Ship: Dragoon
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "falloffEffectiveness",
                                  src.getModifiedItemAttr("shipBonusAD1"), skill="Amarr Destroyer")
