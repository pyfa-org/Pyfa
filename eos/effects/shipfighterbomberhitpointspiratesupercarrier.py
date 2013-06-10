# Used by:
# Ship: Revenant
type = "passive"
def handler(fit, ship, context):
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighter Bombers"),
                                     type, ship.getModifiedItemAttr("shipBonusPirateFaction"))
