# subsystemBonusAmarrPropulsionWarpCapacitor
#
# Used by:
# Subsystem: Legion Propulsion - Interdiction Nullifier
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion"), skill="Amarr Propulsion Systems")
