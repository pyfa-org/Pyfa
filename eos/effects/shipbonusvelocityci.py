# shipBonusVelocityCI
#
# Used by:
# Variations of ship: Tayra (2 of 2)
# Ship: Crane
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusCI"), skill="Caldari Industrial")
