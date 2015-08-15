# shipVelocityBonusAI
#
# Used by:
# Variations of ship: Bestower (2 of 2)
# Ship: Prorator
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusAI"), skill="Amarr Industrial")
