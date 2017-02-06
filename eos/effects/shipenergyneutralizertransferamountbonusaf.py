# shipEnergyNeutralizerTransferAmountBonusAF
#
# Used by:
# Ship: Caedes
# Ship: Cruor
# Ship: Sentinel
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyNeutralizerAmount", ship.getModifiedItemAttr("shipBonusAF"),
                                  skill="Amarr Frigate")
