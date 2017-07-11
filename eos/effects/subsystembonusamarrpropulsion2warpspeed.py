# subsystemBonusAmarrPropulsion2WarpSpeed
#
# Used by:
# Subsystem: Legion Propulsion - Interdiction Nullifier
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion2"),
                           skill="Amarr Propulsion Systems")
