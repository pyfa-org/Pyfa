# shipBonusDroneHitpointsGB2
#
# Used by:
# Variations of ship: Dominix (3 of 3)
# Ship: Dominix Quafe Edition
# Ship: Nestor
# Ship: 多米尼克斯级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                     type, ship.getModifiedItemAttr("shipBonusGB2") * level)
