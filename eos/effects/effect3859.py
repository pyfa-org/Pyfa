# subsystemBonusCaldariPropulsionMaxVelocity
#
# Used by:
# Subsystem: Tengu Propulsion - Chassis Optimization
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("maxVelocity", src.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                           skill="Caldari Propulsion Systems")
