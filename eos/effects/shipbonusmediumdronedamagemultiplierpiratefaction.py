# Used by:
# Ship: Gila
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Medium Drone Operation"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusPirateFaction"))
