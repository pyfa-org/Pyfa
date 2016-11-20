# shipBonusEnergyNosFalloffAC3
#
# Used by:
# Ship: Vangel
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "falloffEffectiveness",
                                  src.getModifiedItemAttr("shipBonusAC3"), skill="Amarr Cruiser")
