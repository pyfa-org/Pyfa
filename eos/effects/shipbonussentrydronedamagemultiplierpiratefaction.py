type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Sentry Drone Interfacing"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusPirateFaction"))
