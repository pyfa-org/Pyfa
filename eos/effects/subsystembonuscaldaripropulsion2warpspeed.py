# subsystemBonusCaldariPropulsion2WarpSpeed
#
# Used by:
# Subsystem: Tengu Propulsion - Interdiction Nullifier
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion2"),
                           skill="Caldari Propulsion Systems")
