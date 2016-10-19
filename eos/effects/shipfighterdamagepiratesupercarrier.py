# shipFighterDamagePirateSupercarrier
#
# Used by:
# Ships from group: Supercarrier (5 of 5)
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Fighters"),
                                 "damageMultiplier", ship.getModifiedItemAttr("shipBonusPirateFaction"))
