# Not used by any item
type = "passive"


def handler(fit, ship, context):
    fit.ship.increaseItemAttr("capacitorCapacity", ship.getModifiedItemAttr("capacitorBonus"))
