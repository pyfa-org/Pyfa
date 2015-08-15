# shipEnergyNeutralizerTransferAmountBonusAB
#
# Used by:
# Ship: Bhaalgorn
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Destabilizer",
                                  "energyDestabilizationAmount", ship.getModifiedItemAttr("shipBonusAB"), skill="Amarr Battleship")
