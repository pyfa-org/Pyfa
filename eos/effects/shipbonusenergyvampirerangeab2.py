# shipBonusEnergyVampireRangeAB2
#
# Used by:
# Ship: Armageddon
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferRange", ship.getModifiedItemAttr("shipBonusAB2"), skill="Amarr Battleship")
