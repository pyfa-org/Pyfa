# shipBonusDreadnoughtA1EnergyWarfareAmountBonus
#
# Used by:
# Ship: Chemosh
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", src.getModifiedItemAttr("shipBonusDreadnoughtA1"), skill="Amarr Dreadnought")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyNeutralizerAmount", src.getModifiedItemAttr("shipBonusDreadnoughtA1"), skill="Amarr Dreadnought")
