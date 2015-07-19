# freighterMaxVelocityBonusM1
#
# Used by:
# Ship: Fenrir
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusM1"), skill="Minmatar Freighter")
