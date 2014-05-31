# Used by:
# Ship: Worm
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Combat Drone Operation"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusPirateFaction"))
