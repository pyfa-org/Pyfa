# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighter Bombers"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusPirateFaction"))
