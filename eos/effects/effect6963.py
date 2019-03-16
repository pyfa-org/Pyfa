# subsystemBonusMinmatarPropulsion2WarpSpeed
#
# Used by:
# Subsystem: Loki Propulsion - Interdiction Nullifier
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion2"),
                           skill="Minmatar Propulsion Systems")
