# freighterCargoBonusC2
#
# Used by:
# Variations of ship: Charon (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusC2"), skill="Caldari Freighter")
