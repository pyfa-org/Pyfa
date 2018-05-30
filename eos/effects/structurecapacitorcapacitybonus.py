# structureCapacitorCapacityBonus
#
# Used by:
# Structure Modules from group: Structure Capacitor Battery (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.ship.increaseItemAttr("capacitorCapacity", ship.getModifiedItemAttr("capacitorBonus"))
