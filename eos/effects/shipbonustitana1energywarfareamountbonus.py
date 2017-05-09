# shipBonusTitanA1EnergyWarfareAmountBonus
#
# Used by:
# Ship: Molok
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", src.getModifiedItemAttr("shipBonusTitanA1"), skill="Amarr Titan")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyNeutralizerAmount", src.getModifiedItemAttr("shipBonusTitanA1"), skill="Amarr Titan")
