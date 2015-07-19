# shipBonusEnergyVampireRangeAD2
#
# Used by:
# Ship: Dragoon
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferRange", ship.getModifiedItemAttr("shipBonusAD2"), skill="Amarr Destroyer")
