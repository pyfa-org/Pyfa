# freighterMaxVelocityBonusA1
#
# Used by:
# Ship: Providence
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusA1"), skill="Amarr Freighter")
