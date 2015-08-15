# freighterMaxVelocityBonusC1
#
# Used by:
# Ship: Charon
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusC1"), skill="Caldari Freighter")
