# subsystemBonusAmarrPropulsionMaxVelocity
#
# Used by:
# Subsystem: Legion Propulsion - Chassis Optimization
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("subsystemBonusAmarrPropulsion"), skill="Amarr Propulsion Systems")
