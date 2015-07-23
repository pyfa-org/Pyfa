# freighterCargoBonusA2
#
# Used by:
# Variations of ship: Providence (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("capacity", ship.getModifiedItemAttr("freighterBonusA2"), skill="Amarr Freighter")
