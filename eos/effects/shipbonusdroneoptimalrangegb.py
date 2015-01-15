# shipBonusDroneOptimalRangeGB
#
# Used by:
# Ship: Dominix
# Ship: Dominix Quafe Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxRange", ship.getModifiedItemAttr("shipBonusGB") * level)
