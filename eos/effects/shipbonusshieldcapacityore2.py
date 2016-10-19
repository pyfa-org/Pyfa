# shipBonusShieldCapacityORE2
#
# Used by:
# Variations of ship: Procurer (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("shieldCapacity", ship.getModifiedItemAttr("shipBonusORE2"), skill="Mining Barge")
