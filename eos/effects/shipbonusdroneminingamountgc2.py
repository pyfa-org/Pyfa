# shipBonusDroneMiningAmountGC2
#
# Used by:
# Ship: Vexor
# Ship: Vexor Navy Issue
type = "passive"


def handler(fit, ship, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Mining Drone",
                                 "miningAmount", ship.getModifiedItemAttr("shipBonusGC2"), skill="Gallente Cruiser")
