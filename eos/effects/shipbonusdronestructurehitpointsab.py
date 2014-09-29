# shipBonusDroneStructureHitPointsAB
#
# Used by:
# Ship: Armageddon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Battleship").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "hp", ship.getModifiedItemAttr("shipBonusAB") * level)
