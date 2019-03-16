# capacitorCapacityBonus
#
# Used by:
# Modules from group: Capacitor Battery (30 of 30)
type = "passive"


def handler(fit, ship, context):
    fit.ship.increaseItemAttr("capacitorCapacity", ship.getModifiedItemAttr("capacitorBonus"))
