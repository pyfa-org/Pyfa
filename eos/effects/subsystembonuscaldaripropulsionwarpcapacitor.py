# subsystemBonusCaldariPropulsionWarpCapacitor
#
# Used by:
# Subsystem: Tengu Propulsion - Interdiction Nullifier
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("warpCapacitorNeed", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                           skill="Caldari Propulsion Systems")
