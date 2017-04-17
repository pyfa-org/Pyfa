# shipBonusDroneMWDboostrole
#
# Used by:
# Ship: Algos
# Ship: Dragoon
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "maxVelocity", ship.getModifiedItemAttr("shipBonusRole7"))
