# Used by:
# Variations of ship: Myrmidon (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battlecruiser").level
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusGBC1") * level)
