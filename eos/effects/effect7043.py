# shipShieldHitpointsCC1
#
# Used by:
# Ship: Monitor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldCapacity", src.getModifiedItemAttr("shipBonusCC"), skill="Caldari Cruiser")
