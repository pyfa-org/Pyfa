# shipBonusEnergyNosOptimalAD2
#
# Used by:
# Ship: Dragoon
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "maxRange",
                                  src.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
