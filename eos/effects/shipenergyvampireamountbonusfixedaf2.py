# shipEnergyVampireAmountBonusFixedAF2
#
# Used by:
# Ship: Malice
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferAmount", ship.getModifiedItemAttr("shipBonus2AF"), skill="Amarr Frigate")
