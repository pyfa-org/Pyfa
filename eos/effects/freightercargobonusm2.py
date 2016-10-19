# freighterCargoBonusM2
#
# Used by:
# Variations of ship: Fenrir (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusM2"), skill="Minmatar Freighter")
