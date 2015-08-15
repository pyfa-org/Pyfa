# freighterCargoBonusG2
#
# Used by:
# Variations of ship: Obelisk (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusG2"), skill="Gallente Freighter")
