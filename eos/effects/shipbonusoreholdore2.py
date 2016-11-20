# shipBonusOreHoldORE2
#
# Used by:
# Variations of ship: Retriever (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("specialOreHoldCapacity", ship.getModifiedItemAttr("shipBonusORE2"), skill="Mining Barge")
