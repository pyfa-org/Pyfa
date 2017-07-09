# subsystemBonusCaldariPropulsionWarpSpeed
#
# Used by:
# Subsystem: Tengu Propulsion - Chassis Optimization
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("baseWarpSpeed", module.getModifiedItemAttr("subsystemBonusCaldariPropulsion"),
                           skill="Caldari Propulsion Systems")
