# shipVelocityBonusRookie
#
# Used by:
# Ship: Reaper
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("maxVelocity", ship.getModifiedItemAttr("rookieShipVelocityBonus"))
