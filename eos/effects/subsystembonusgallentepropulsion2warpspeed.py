# subsystemBonusGallentePropulsion2WarpSpeed
#
# Used by:
# Subsystem: Proteus Propulsion - Interdiction Nullifier
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpSpeedMultiplier", src.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                           skill="Gallente Propulsion Systems")
