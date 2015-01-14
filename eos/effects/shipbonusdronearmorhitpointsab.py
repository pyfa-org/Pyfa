# shipBonusDroneArmorHitPointsAB
#
# Used by:
# Ship: Armageddon
# Ship: 末日沙场级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "armorHP", ship.getModifiedItemAttr("shipBonusAB") * level)
