# freighterMaxVelocityBonusG1
#
# Used by:
# Ship: Obelisk
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("freighterBonusG1"), skill="Gallente Freighter")
