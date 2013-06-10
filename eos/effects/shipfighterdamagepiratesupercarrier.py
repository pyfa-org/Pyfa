# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighters"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusPirateFaction"))
