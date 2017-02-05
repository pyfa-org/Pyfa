# shipBonusNosOptimalFalloffAC2
#
# Used by:
# Ship: Rabisu
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                  src.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                  src.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
