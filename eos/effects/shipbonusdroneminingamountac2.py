# shipBonusDroneMiningAmountAC2
#
# Used by:
# Ship: Arbitrator
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                 "miningAmount", ship.getModifiedItemAttr("shipBonusAC2"), skill="Amarr Cruiser")
