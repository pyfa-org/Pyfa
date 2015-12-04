# shipEnergyNeutralizerTransferAmountBonusAC
#
# Used by:
# Ship: Ashimmu
# Ship: Vangel
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Neutralizer",
                                  "energyDestabilizationAmount", ship.getModifiedItemAttr("shipBonusAC"), skill="Amarr Cruiser")
