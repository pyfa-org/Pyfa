# subsystemBonusMinmatarPropulsionMaxVelocity
#
# Used by:
# Subsystem: Loki Propulsion - Intercalated Nanofibers
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("subsystemBonusMinmatarPropulsion"),
                           skill="Minmatar Propulsion Systems")
