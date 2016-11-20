# shipEnergyDrainAmountAF1
#
# Used by:
# Ship: Cruor
# Ship: Sentinel
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu",
                                  "powerTransferAmount", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
