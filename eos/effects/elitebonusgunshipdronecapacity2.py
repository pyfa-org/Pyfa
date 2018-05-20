# Not used by any item
type = "passive"


def handler(fit, ship, context):
    fit.ship.increaseItemAttr("droneCapacity", ship.getModifiedItemAttr("eliteBonusGunship2"), skill="Assault Frigates")
