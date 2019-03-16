# shipBonusEnergyNeutOptimalAF2
#
# Used by:
# Ship: Malice
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer", "maxRange",
                                  src.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
