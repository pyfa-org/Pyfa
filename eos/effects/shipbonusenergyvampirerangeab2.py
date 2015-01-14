# shipBonusEnergyVampireRangeAB2
#
# Used by:
# Ship: Armageddon
# Ship: 末日沙场级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Vampire",
                                  "powerTransferRange", ship.getModifiedItemAttr("shipBonusAB2") * level)
