# shipFighterHitpointsPirateSupercarrier
#
# Used by:
# Ships from group: Supercarrier (5 of 5)
type = "passive"
def handler(fit, ship, context):
    for type in ("shieldCapacity", "armorHP", "hp"):
        fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighters"),
                                     type, ship.getModifiedItemAttr("shipBonusPirateFaction"))
