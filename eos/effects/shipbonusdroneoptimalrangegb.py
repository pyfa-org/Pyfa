# shipBonusDroneOptimalRangeGB
#
# Used by:
# Ship: Dominix
# Ship: Dominix Quafe Edition
# Ship: 多米尼克斯级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxRange", ship.getModifiedItemAttr("shipBonusGB") * level)
