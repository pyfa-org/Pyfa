# subsystemBonusGallentePropulsionWarpSpeed
#
# Used by:
# Subsystem: Proteus Propulsion - Chassis Optimization
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("baseWarpSpeed", module.getModifiedItemAttr("subsystemBonusGallentePropulsion"),
                           skill="Gallente Propulsion Systems")
