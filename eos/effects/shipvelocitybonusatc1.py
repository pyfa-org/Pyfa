# Used by:
# Ship: Adrestia
# Ship: Mimir
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("shipBonusATC1"))
