# capacitorCapacityBonus
#
# Used by:
# Modules from group: Capacitor Battery (22 of 22)
type = "passive"
def handler(fit, ship, context):
    fit.ship.increaseItemAttr("capacitorCapacity", ship.getModifiedItemAttr("capacitorBonus"))