type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Combat Drone Operation"),
                                 "hp", ship.getModifiedItemAttr("shipBonusPirateFaction"))
